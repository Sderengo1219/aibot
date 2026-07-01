import os
from config import MAX_CHARS
from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Provides the contents of a file in the format of a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file from which the contents will be retrieved, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
