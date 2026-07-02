import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:    
        working_dir_abs = os.path.abspath(working_directory)

        full_path = os.path.join(working_dir_abs, file_path)
        full_path = os.path.normpath(full_path)

        if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]

        if args:
            command.extend(args)

        process_complete = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        output_parts = []

        if process_complete.returncode != 0:
            output_parts.append(f"Process exited with code {process_complete.returncode}")
        if not process_complete.stdout and not process_complete.stderr:
            output_parts.append("No output produced")
        if process_complete.stdout:
            output_parts.append(f"STDOUT: {process_complete.stdout}")
        if process_complete.stderr:
            output_parts.append(f"STDERR: {process_complete.stderr}")

        output_string = "\n".join(output_parts)

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the Python file located at the provided file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the Python file to be run",
                },
                "args": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    },
                    "description": "list of command line arguments each element in list with be a string",
                },
            },
        },
    },
}