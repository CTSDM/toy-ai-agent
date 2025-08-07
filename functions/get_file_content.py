import os
from functions.checks import check_path_inside, check_file_exist
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    check_path = check_path_inside(file_path)
    if check_path:
        return check_path
    check_file = check_file_exist(working_directory, file_path)
    if check_file:
        return check_file

    try:
        dir_abs = os.path.abspath(working_directory + "/" + file_path)
        with open(dir_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[:-1] + (
                f'[...File "{dir_abs}" truncated at ${MAX_CHARS} characters].'
            )
        return file_content_string

    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Lists the content of the file in the specified directory. In case the text is longer than {MAX_CHARS} the content gets truncated.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to get the content from, relative to the working directory. If not provided, there will be an error.",
            ),
        },
    ),
)
