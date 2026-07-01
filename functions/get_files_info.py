import os
from google.genai import types

def get_files_info(working_directory: str, directory: str = ".") -> str:
        
    try:    
        working_dir_abs = os.path.abspath(working_directory)

        full_path = os.path.join(working_dir_abs, directory)
        full_path = os.path.normpath(full_path)

        if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        list_directory_contents = os.listdir(full_path)
        
        if directory == ".":
            lines = ["Result for current directory:"]
        else:
            lines = [f"Result for '{directory}' directory"]

        for item in list_directory_contents:
            item_name = item
            item_size = os.path.getsize(os.path.join(full_path, item))
            is_dir = os.path.isdir(os.path.join(full_path, item))
            lines.append(f"  - {item_name}: file_size={item_size} bytes, is_dir={is_dir}")

        return_variable = "\n".join(lines)
        return return_variable

    except Exception as e:
        return f"Error: {str(e)}"



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
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

    