# functions/get_files_info.py 

import os 


def get_files_info(working_directory, directory="."):

    try:

        is_valid_dir = os.path.isdir(directory)
        if not is_valid_dir:
            return f'Error: "{directory}" is not a directory'

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if valid_target_dir == True:
            return f'Success: "{directory}" is within the working directory'
    
    except Exception as e:
        return f'Error: there was an issue validating directories: {e}'


