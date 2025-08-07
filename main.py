import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <prompt> [--verbose]")
        sys.exit(1)

    client = get_aiclient()
    contents = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=contents)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )
    print("Hello from toy-ai-agent!")
    print(response.text)

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        print("User prompt:", contents)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


def get_aiclient():
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


if __name__ == "__main__":
    main()
