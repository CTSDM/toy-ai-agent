from functions.checks import check_file_exist, check_path_inside
from config import TIMEOUT
import functions.constants as constants
import os, subprocess


def run_python_file(working_directory, file_path, args=[]):
    check_path = check_path_inside(
        file_path, constants.ERROR_RUN_OUTSIDE_WORKING_DIRECTORY
    )
    if check_path:
        return check_path
    check_file = check_file_exist(
        working_directory, file_path, constants.ERROR_RUN_NOT_FOUND
    )
    if check_file:
        return check_file

    try:
        dir_abs = os.path.abspath(working_directory + "/" + file_path)
        if file_path[-3:] != ".py":
            return constants.ERROR_RUN_NOT_PY.replace("$$$", dir_abs)
        result = subprocess.run(
            ["python", dir_abs, *args], timeout=TIMEOUT, capture_output=True
        )
        print(result)
        if result:
            return f"STDOUT: {result.stdout}, STDERR: {result.stderr}, Process exited with code {result.returncode}"
        return "No output produced"
    except Exception as e:
        return f"Error: executing Python file {e}"
