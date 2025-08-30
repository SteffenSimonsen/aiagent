import os
from google.genai import types

def get_files_info(working_directory, directory="."):

    full_path = os.path.join(working_directory, directory)
    
    abs_working_dir = os.path.abspath(working_directory)

    abs_target_path = os.path.abspath(full_path)
   
    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: (file: get_files_info) Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: (file: get_files_info) "{directory}" is not a directory'

    list_dir = os.listdir(full_path)

    results = []
    for name in list_dir:
        try:
            path = os.path.join(full_path, name)
            results.append(f"- {name}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")
        except Exception as e:
            return f"Error: (file: get_files_info) {e}"

    return "\n".join(results)


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
