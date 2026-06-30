import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
        
    try:    
        working_dir_abs = os.path.abspath(working_directory)

        full_path = os.path.join(working_dir_abs, directory)
        full_path = os.path.normpath(full_path)

        if os.path.commonpath([working_dir_abs, full_path]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {str(e)}"