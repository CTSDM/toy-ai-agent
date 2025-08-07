import os
from functions.checks import check_path_inside
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        dir_abs = os.path.abspath(working_directory + "/" + file_path)
        checks = check_path_inside(working_directory, file_path)
        if checks:
            return checks
        with open(dir_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{dir_abs}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content into the specified file. If the file does not exist it gets created.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write the content into",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)
