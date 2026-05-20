# functions/get_file_content.py 

import os 
import sys 

from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(root_dir))

from config import MAX_CHARS_TO_READ_FROM_FILE

def get_file_content(working_directory, file_path):


    try:
        working_dir_abs = os.path.abspath(working_directory)
        
        file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
        is_file = os.path.isfile(file_path_abs)

        is_valid = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs

        if not is_valid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not is_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:

            file_content_string = f.read(MAX_CHARS_TO_READ_FROM_FILE)
    
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ_FROM_FILE} characters]'

        return file_content_string

    except Exception as e:
            return f'Error: the contents of {file_path} could not be read: {e}'



