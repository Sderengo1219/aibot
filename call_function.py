import json
from collections.abc import Callable
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call, verbose: bool = False):

    function_name = function_call.function.name or ""

    if verbose:
        print(f"Calling function: {function_name}({function_call.function.arguments})")
    else:
        print(f" - Calling function: {function_name}")


    if function_name not in function_map:
        return {
            "role": "tool",
            "tool_call_id": function_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }
    
    args = json.loads(function_call.function.arguments or "{}")

    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return {
        "role": "tool",
        "tool_call_id": function_call.id,
        "content": function_result,
    }