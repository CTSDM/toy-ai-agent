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

from config import SYSTEMP_PROMPT, MAX_CALLS_AGENT

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
    verbose = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose = True

    for _ in range(MAX_CALLS_AGENT):
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=SYSTEMP_PROMPT
            ),
        )

        # we add all the responses to the messages to have context
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # if there are no more function calls, it is safe to assume we have a final answer
        if not response.function_calls:
            if response.text:
                print("Final response")
                print(response.text)
                return
            if verbose:
                print("User prompt:", contents)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

        try:
            function_responses = []
            # let's handle the function calls
            # we need to call all the functions available
            for function_call in response.function_calls:
                function_response = call_function(function_call, verbose)

                if (
                    not function_response.parts
                    or not function_response.parts[0].function_response
                ):
                    raise Exception("empty function call result")

                function_responses.append(function_response.parts[0])

            messages.append(types.Content(role="tool", parts=function_responses))

        except Exception as e:
            print(f'Error: "{e}"')
            raise

    print(
        f"Max calls to the agent ({MAX_CALLS_AGENT}) have been reached without having an answer..."
    )


def get_aiclient():
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


if __name__ == "__main__":
    main()
