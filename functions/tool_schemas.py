# functions.tool_schemas 

from google.genai import types



# Tool Schema for functions.get_files_info.py / get_files_info() function - Google Genai (Gemini SDK Tool Schema - FunctionDeclaration)
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="List files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

# Tool Schema for functions.get_file_content.py / get_file_content() function - Google Genai (Gemini SDK Tool Schema - FunctionDeclaration)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get the contents of a specific file (Read File). You can only read files within the current working directory (injected by default), and it's subdirectories. It is strongly recommended to use the get_files_info tool first to list the files in a directory, then call this function with the file_path param, file_path must be relative to the working directory, to read the contents of the file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory. For files in the working directory file_path is just the file name, for files in a subdirectory of the working directory provide the path with no leading slash, e.g. `dir/filename.txt` or `other_sub_dir/other_file_name.py`.",
            ),
        },
    ),
)

# Tool Schema for functions.write_file.py / write_file() function - Google Genai (Gemini SDK Tool Schema - FunctionDeclaration)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="The write_file tool can either write a new file, or overwrite an existing file's content. The file to write/replace contents must be either in the working directory or subdirectories of the working directory. The file_path param should be the file name for a file in the working directory, or path to the file relative to the working directory with no leading slash. e.g. `filename.py` or `dir/filename.py` or `sub_dir_first/sub_dir_second/filename.py` - When writing a new file, nested subdirectories will be automatically created if not exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File name or path to file relative to the working directory to create or overwrite.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to file, as a string. When writing to an existing file the content provided will completely replace the existing contents of the file, currently there is no way to partially edit an existing file with this tool.",
            ),
        },
    ),
)

# Tool Schema for functions.run_python_file.py / run_python_file() function - Google Genai (Gemini SDK Tool Schema - FunctionDeclaration)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file/script and get the results. This tool provides you the ability to write your own tools as python scripts with the write_file tool, then run them with this tool and receive the results. You can also run existing python files within the working directory or it's subdirectories to get the results or troubleshoot errors. The rturned results will include, when available, the returncode, stdout, and stderr from the script.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File name or path to file (Python Files Only '.py') relative to the working directory. The run_python_file file's file_path param MUST be an existing file in the working directory or it's subdirectories, if you need to create a python script use the write_file tool first, then call the Python script with this tool to get it's results.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional array of arguments to pass to the Python Script being called.",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },

    ),

)



# INDEX of all Tools Schemas to pass the Google Genai GenerateContentConfig (in root main.py)
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
)
