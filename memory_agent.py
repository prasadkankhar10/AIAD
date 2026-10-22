import argparse
import os
import sys
from typing import List, Dict

sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
from openai import OpenAI

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "groq/compound"

class SlidingWindowMemoryAgent:
    """
    An AI agent that maintains a short-term conversational memory using a sliding window.
    It remembers a maximum number of recent message pairs (User + Assistant) to manage context length.
    """
    def __init__(self, client: OpenAI, model: str, max_pairs: int = 2):
        self.client = client
        self.model = model
        self.max_pairs = max_pairs
        
        # System prompt is always preserved
        self.system_prompt = {
            "role": "system",
            "content": "You are a helpful, conversational AI assistant. You have a short-term memory limit."
        }
        
        # History stores only the User and Assistant exchanges
        self.history: List[Dict[str, str]] = []

    def get_context(self) -> List[Dict[str, str]]:
        """Construct the full message list for the LLM based on the sliding window."""
        # A pair is 2 messages (User, Assistant). max_pairs * 2 is max messages.
        # Since this is called right after a user message is appended,
        # the history length is odd (User, Asst, User, Asst, User).
        # We want the pruned history to start with a User message.
        # If we want to keep max_pairs of context (plus the current user message),
        # we should keep (max_pairs * 2) + 1 messages maximum.
        max_messages_to_keep = (self.max_pairs * 2) + 1
        
        pruned_history = self.history[-max_messages_to_keep:] if len(self.history) > max_messages_to_keep else self.history
        
        return [self.system_prompt] + pruned_history

    def chat(self, user_input: str) -> str:
        """Process a user message, query the LLM, and update memory."""
        # 1. Add user input to history
        self.history.append({"role": "user", "content": user_input})
        
        # 2. Get the pruned context window
        messages_for_llm = self.get_context()
        
        # 3. Call the LLM
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages_for_llm,
            temperature=0.7,
        )
        response_text = completion.choices[0].message.content or ""
        
        # 4. Add assistant response to history
        self.history.append({"role": "assistant", "content": response_text})
        
        return response_text

def main() -> None:
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Memory Agent with Sliding Window")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model name to use")
    parser.add_argument("--window", type=int, default=2, help="Number of conversation pairs to remember")
    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("Missing GROQ_API_KEY in environment or .env file.")
        
    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    
    # Initialize the agent with memory
    agent = SlidingWindowMemoryAgent(client=client, model=args.model, max_pairs=args.window)

    print(f"[Memory Agent] loaded (Model: {args.model}, Memory Window: {args.window} pairs).")
    print("Type your message. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            break
            
        if not user_input:
            continue
            
        if user_input.lower() in {"exit", "quit", "bye"}:
            print("Exiting chat.")
            break
            
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    main()
