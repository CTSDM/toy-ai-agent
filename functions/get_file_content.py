import os
from functions.checks import check_path_inside, check_file_exist
from config import MAX_CHARS


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
