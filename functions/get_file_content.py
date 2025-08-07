import os
from functions.checks import check_path
from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    check_result = check_path(working_directory, file_path, True)
    if check_result:
        return check_result

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
