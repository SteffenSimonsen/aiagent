import os
from google.genai import types

def write_file(working_directory, file_path, content):

    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)

    abs_target_path = os.path.abspath(full_path)

    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: (file: write_file) Cannot read "{file_path}" as it is outside the permitted working directory'

    dir_name = os.path.dirname(abs_target_path)
    
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        
        with open(abs_target_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f"Error: (file: write_file) {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the file specified by file_path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file, to which the function should write the content",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file",
            ),
        },
    ),
)
