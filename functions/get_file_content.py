import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
        
    try:    
        working_dir_abs = os.path.abspath(working_directory)

        full_path = os.path.join(working_dir_abs, file_path)
        full_path = os.path.normpath(full_path)

        if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{full_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string

    except Exception as e:
        return f"Error: {str(e)}"
