# functions/run_python_file.py 

import os 
import subprocess


def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:

        working_dir_abs = os.path.normpath(os.path.abspath(working_directory))
        file_path_abs = os.path.normpath(os.path.abspath(os.path.join(working_dir_abs, file_path)))
        is_file = os.path.isfile(file_path_abs)
        is_valid = os.path.commonpath([working_dir_abs, file_path_abs]) == working_dir_abs
        py_file_ext = file_path_abs[-3:]

        if not is_valid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if py_file_ext != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]

        if args:
            command.extend(args)

        res = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )

        if res.returncode != 0:
            return f'Process exited with code {res.returncode}'

        response = f'Results from "{file_path}": \n'

        if not res.stdout and not res.stderr:
            response += f'No output produced \n'

        if res.stdout:
            response += f'STDOUT: {res.stdout} \n\n'

        if res.stderr:
            response += f'STDERR: {res.stderr}'

        return response

    except Exception as e:
        return f'Error: executing Python file: {e}'

