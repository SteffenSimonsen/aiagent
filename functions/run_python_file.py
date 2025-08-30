import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):

    full_path = os.path.join(working_directory, file_path)

    abs_working_dir = os.path.abspath(working_directory)

    abs_target_path = os.path.abspath(full_path)

    if not abs_target_path.startswith(abs_working_dir):
        return f'Error: (file: run_python_file) Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: (file: run_python_file) File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: (file: run_python_file) "{file_path}" is not a Python file.'
    
    try:
        cmd = ["python", file_path, *args]
        completed_process = subprocess.run(
                        cmd,
                        timeout=30,
                        capture_output=True,
                        cwd=working_directory,
                        text=True
        )
    except Exception as e:
        return f"Error: (file: run_python_file) executing Python file: {e}"  
      

    stdout = completed_process.stdout or ""
    stderr = completed_process.stderr or ""

    if not stdout and not stderr:
        return "No output produced"
    
    parts = [f"STDOUT: \n{stdout.strip()}", f"STDERR: \n{stderr.strip()}"]


    if not completed_process.returncode == 0:
        parts.append(f"Process exited with code {completed_process.returncode}")
    
    return "\n".join(parts)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file, which should be run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The args parameter contains OPTIONAL CLI arguments."
            )
        },
        required=["file_path"]
    ),
)
