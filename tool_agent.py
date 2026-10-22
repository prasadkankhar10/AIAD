import argparse
import json
import os
import sys
import ast
import operator
import math

sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
from openai import OpenAI

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "openai/gpt-oss-20b"

# ==========================================
# 1. Define the actual Tool Functions (Python)
# ==========================================

def calculate(expression: str) -> str:
    """Evaluates a mathematical expression safely."""
    print(f"  [Tool Execution] Calculating: {expression}")
    
    # Supported operators
    ops = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.BitXor: operator.xor,
        ast.USub: operator.neg
    }

    def eval_node(node):
        if isinstance(node, ast.Constant): # <number>
            return node.value
        elif isinstance(node, ast.BinOp): # <left> <operator> <right>
            return ops[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
            return ops[type(node.op)](eval_node(node.operand))
        else:
            raise TypeError(node)
            
    try:
        node = ast.parse(expression, mode='eval').body
        result = eval_node(node)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def read_file(filepath: str) -> str:
    """Reads the contents of a local file."""
    print(f"  [Tool Execution] Reading file: {filepath}")
    try:
        if not os.path.exists(filepath):
            return f"Error: File '{filepath}' not found."
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Truncate if it's too long just to save tokens
            if len(content) > 2000:
                return content[:2000] + "\n...[Content Truncated]..."
            return content
    except Exception as e:
        return f"Error reading file: {e}"

# Map tool names to functions
AVAILABLE_TOOLS = {
    "calculate": calculate,
    "read_file": read_file
}

# ==========================================
# 2. Define the Tool Schemas (JSON)
# ==========================================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression (e.g., '2 + 2', '453 * 19', '10 / 2').",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a local file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "The path to the file to read (e.g., 'requirements.txt')."
                    }
                },
                "required": ["filepath"]
            }
        }
    }
]

# ==========================================
# 3. Implement the Tool-Enabled Agent
# ==========================================

def chat_with_tools(client: OpenAI, model: str, user_input: str, messages: list) -> str:
    messages.append({"role": "user", "content": user_input})
    
    # First call: LLM decides whether to use a tool or answer directly
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS_SCHEMA,
        tool_choice="auto",
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # If the LLM didn't request a tool, return its answer directly
    if not tool_calls:
        msg = response_message.content or ""
        messages.append({"role": "assistant", "content": msg})
        return msg
        
    # If the LLM requested tools, we must execute them
    messages.append(response_message)  # Append the assistant's tool call request
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        # Execute the requested function
        function_to_call = AVAILABLE_TOOLS.get(function_name)
        if function_to_call:
            if function_name == "calculate":
                function_response = function_to_call(expression=function_args.get("expression"))
            elif function_name == "read_file":
                function_response = function_to_call(filepath=function_args.get("filepath"))
            
            # Send the result back to the LLM
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
            
    # Second call: LLM generates final response based on tool output
    second_response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    
    final_msg = second_response.choices[0].message.content or ""
    messages.append({"role": "assistant", "content": final_msg})
    return final_msg

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Tool-Enabled Agent")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model to use")
    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("Missing GROQ_API_KEY in environment or .env file.")
        
    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to tools. Always use the tools available when appropriate to answer user queries."}
    ]
    
    print(f"[Tool-Enabled Agent] loaded (Model: {args.model}).")
    print("Available tools: Calculator, File Reader")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "bye"]:
                break
                
            response = chat_with_tools(client, args.model, user_input, messages)
            print(f"Agent: {response}\n")
            
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            break
        except Exception as e:
            print(f"\n[Error] {e}")

if __name__ == "__main__":
    main()
