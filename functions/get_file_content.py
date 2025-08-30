import os
from functions.config import MAX_CHARS
from google.genai import types



def get_file_content(working_directory, file_path):

    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)

    abs_target_path = os.path.abspath(full_path)

    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: (file: get_file_content) Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(full_path):
        return f'Error: (file: get_file_content) File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, "r") as f:
            content = f.read()
        
        pre_len = len(content)

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters'
        
        post_len = len(content)

        if not pre_len == post_len:
            print(f"Truncated content of {file_path} from {pre_len} to {post_len} characters")

        return content
    
    except Exception as e:
        return f"Error: (file: get_file_content) {e}"

   
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of the file specified by file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file, from which the function should retrieve the content",
            ),
        },
    ),
)
