from __future__ import annotations

import argparse
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
from openai import OpenAI


GROQ_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "groq/compound"


def build_client(api_key: str | None) -> OpenAI:
    if not api_key:
        raise SystemExit(
            "Missing GROQ_API_KEY. Set it in your environment or in a local .env file."
        )

    return OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)


def generate_response(client: OpenAI, model: str, messages: list[dict[str, str]]) -> str:
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )

    return completion.choices[0].message.content or ""


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Chat with an LLM using Groq's OpenAI-compatible API."
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model name to use")
    args = parser.parse_args()

    api_key = os.getenv("GROQ_API_KEY")
    client = build_client(api_key)

    messages = [
        {
            "role": "system",
            "content": "You are a concise and helpful assistant.",
        }
    ]

    print("Groq chat is ready. Type /exit to quit.")

    while True:
        try:
            prompt = input("You: ").strip()
        except EOFError:
            print("\nExiting chat.")
            break

        if not prompt:
            continue
        if prompt.lower() in {"/exit", "exit", "quit"}:
            print("Exiting chat.")
            break

        messages.append({"role": "user", "content": prompt})
        response_text = generate_response(client, args.model, messages)
        messages.append({"role": "assistant", "content": response_text})

        print(f"Assistant: {response_text}")


if __name__ == "__main__":
    main()