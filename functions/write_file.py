# functions/write_file.py 

import os 


def write_file(working_directory: str, file_path: str, content: str) -> str:


    try:

        working_dir_abs = os.path.normpath(os.path.abspath(working_directory))
        file_path_abs = os.path.normpath(os.path.abspath(os.path.join(working_dir_abs, file_path)))
        is_file = os.path.isfile(file_path_abs)
        is_dir = os.path.isdir(file_path_abs)
        is_valid = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_valid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Get Parent Dir 
        parent_dir = os.path.dirname(file_path_abs)

        # Create Parent Dirs 
        os.makedirs(parent_dir, exist_ok=True)

        # Write the File 
        with open(file_path_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: there was an issue when attempting to write {file_path}: {e}'




        

