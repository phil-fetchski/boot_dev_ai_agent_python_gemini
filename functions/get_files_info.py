# functions/get_files_info.py 

import os
from datetime import datetime


def get_files_info(working_directory, directory="."):

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        is_valid_dir = os.path.isdir(target_dir)
        if not is_valid_dir:
            return f'Error: "{directory}" is not a directory'

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
    
    except Exception as e:
        return f'Error: there was an issue validating directories: {e}'

    try:
        if is_valid_dir and valid_target_dir:
            
            dir_list = os.listdir(target_dir)
            
            dir_info_tups = []

            dir_fmt = "current" if directory == "." else f"'{directory}'"

            dir_res_string = f"Result for {dir_fmt} directory:"

            for i in dir_list:
                i_path = os.path.normpath(os.path.join(target_dir, i))
                is_dir = os.path.isdir(i_path)
                i_size = os.path.getsize(i_path)
                dir_info_tups.append(("  ", f"- {i}:", f"file_size={i_size} bytes", f"is_dir={is_dir}"))

            res_str = "\n".join(f"{t[0]}{t[1]} {t[2]}, {t[3]}" for t in dir_info_tups)

            res = dir_res_string + "\n" + res_str

            return res

               
    except Exception as e:
        return f'Error: error in get info files: {e}'




