# functions.call_function.py 

from google.genai import types 
from collections.abc import Callable
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

# Definitive Function Map - No Call if not in Map. import into main.py and check for fc in function_calls[] against this dict
FUNCTION_MAP: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(
        function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in FUNCTION_MAP:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    if function_name in FUNCTION_MAP:

        func_args = dict(function_call.args) if function_call.args else {}

        # SET WORKING DIRECTORY FOR FUNCTION CALLS
        func_args["working_directory"] = "./calculator"

        func_result: str = FUNCTION_MAP[function_name](**func_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": func_result},
                )
            ],
        )


