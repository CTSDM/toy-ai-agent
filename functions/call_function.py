from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # manually add the working directory
    function_call_part.args["working_directory"] = "./calculator"
    function_name = function_call_part.name
    args = function_call_part.args

    function_result = None
    match function_name:
        case "get_file_content":
            function_result = get_file_content(**args)
        case "get_files_info":
            function_result = get_files_info(**args)
        case "run_python_file":
            function_result = run_python_file(**args)
        case "write_file":
            function_result = write_file(**args)
        case _:
            raise Exception("Error: no function from the list was called")

    if isinstance(function_result, str):
        if function_result.startswith("Error"):
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
