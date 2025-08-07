import os
import functions.constants as constants


def check_path_inside(directory, msg=constants.ERROR_OUTSIDE_WORKING_DIRECTORY):
    if directory.startswith("..") or directory.startswith("/"):
        error_message = msg.replace("$$$", directory)
        return error_message
    return None


def check_dir_exist(working_directory, directory):
    dir_abs = os.path.abspath(working_directory + "/" + directory)
    if not os.path.isdir(dir_abs):
        return constants.ERROR_NOT_DIRECTORY.replace("$$$", directory)

    return None


def check_file_exist(working_directory, file_path, msg=constants.ERROR_NOT_FILE):
    dir_abs = os.path.abspath(working_directory + "/" + file_path)
    if not os.path.isfile(dir_abs):
        return msg.replace("$$$", file_path)
