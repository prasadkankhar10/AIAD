import argparse
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from openai import OpenAI


GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "groq/compound"

# 1. Design Effective Prompts for Task-Oriented Agents
SYSTEM_PROMPT = """
You are an expert Senior Software Engineer and Code Explainer.
Your task is to take a code snippet from the user and explain how it works.

You must ALWAYS format your response exactly according to the following structure:

### 1. Purpose
[Provide a clear, 1-2 sentence summary of what the code does]

### 2. Step-by-Step Logic
[Provide a bulleted list explaining the key logic of the code]

### 3. Complexity
- **Time Complexity:** [Big O notation with brief explanation]
- **Space Complexity:** [Big O notation with brief explanation]

### 4. Edge Cases / Improvements
[List any potential bugs, unhandled edge cases, or optimizations]

Do not include any conversational filler like "Sure, I can help with that!" or "Here is the explanation". 
Strictly stick to the output format.
"""

def build_client(api_key: str | None) -> OpenAI:
    if not api_key:
        raise SystemExit(
            "Missing GROQ_API_KEY. Set it in your environment or in a local .env file."
        )
    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)

def generate_explanation(client: OpenAI, model: str, code_snippet: str) -> str:
    # 2. Implementing a prompt-based AI agent using an LLM
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Please explain this code:\n\n{code_snippet}"}
    ]

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2, # Low temperature for more deterministic/factual output
    )

    return completion.choices[0].message.content or ""

def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="A Prompt-Driven Code Explainer Agent using Groq API."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model name to use")
    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    client = build_client(api_key)

    print(f"[Code Explainer Agent] loaded (Model: {args.model}).")
    print("Paste your code below. Type 'DONE' on a new line when finished pasting, or 'EXIT' to quit.")

    while True:
        try:
            print("\n" + "="*50)
            print("Your Code:")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == "EXIT":
                    print("\nExiting Code Explainer.")
                    return
                if line.strip().upper() == "DONE":
                    break
                lines.append(line)
            
            code_snippet = "\n".join(lines).strip()
            
            if not code_snippet:
                print("No code provided. Try again.")
                continue

            print("\nAnalyzing code...\n")
            explanation = generate_explanation(client, args.model, code_snippet)
            
            print("--- EXPLANATION ---")
            print(explanation)
            print("-------------------")

        except EOFError:
            print("\nExiting Code Explainer.")
            break
        except KeyboardInterrupt:
            print("\nExiting Code Explainer.")
            break

if __name__ == "__main__":
    main()
