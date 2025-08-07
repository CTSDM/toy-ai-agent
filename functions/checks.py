import os
import functions.constants as constants


def check_path(working_directory, directory, is_file=False):
    dir_abs = os.path.abspath(working_directory + "/" + directory)
    if directory.startswith("..") or directory.startswith("/"):
        error_message = constants.ERROR_OUTSIDE_WORKING_DIRECTORY.replace(
            "$$$", dir_abs
        )
        return error_message
    if is_file:
        if not os.path.isfile(dir_abs):
            return constants.ERROR_NOT_FILE.replace("$$$", dir_abs)
    else:
        if not os.path.isdir(dir_abs):
            return constants.ERROR_NOT_DIRECTORY.replace("$$$", dir_abs)

    return None
