import os
from functions.checks import check_path_inside, check_dir_exist


def get_files_info(working_directory, directory="."):
    try:
        check_path = check_path_inside(directory)
        if check_path:
            return check_path
        check_dir = check_dir_exist(working_directory, directory)
        if check_dir:
            return check_dir

        dir_abs = os.path.abspath(working_directory + "/" + directory)
        dir_info = []
        for item in os.listdir(dir_abs):
            item_size = os.path.getsize(dir_abs + "/" + item)
            item_is_file = os.path.isfile(dir_abs + "/" + item)
            dir_info.append(
                f"{item}: file_size={item_size} bytes, is_dir={item_is_file}"
            )

        return "\n".join(dir_info)

    except Exception as e:
        return e
