import os
from functions.checks import check_path_inside


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
