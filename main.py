import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

from config import SYSTEMP_PROMPT

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
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEMP_PROMPT
        ),
    )

    # updating verbose flag if necessary
    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    print("Hello from toy-ai-agent!")
    if response != None:
        try:
            function_call = response.function_calls
            function_call_result = None
            if function_call:
                function_call_result = call_function(function_call[0], verbose)
            else:
                print(response.text)

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
                print("User prompt:", contents)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

        except Exception as e:
            print(f'Error: "{e}"')


def get_aiclient():
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


if __name__ == "__main__":
    main()
