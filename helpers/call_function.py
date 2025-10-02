from google.genai import types

from helpers.schemas import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_run_python_file,
        schema_get_file_content,
        schema_write_file
    ]
)

def call_function(function_call_part, verbose=False):
    func_name = function_call_part.name
    args = dict(function_call_part.args)

    if verbose:
        print(f"Calling function: {func_name}({args})")
    else:
        print(f" - Calling function: {func_name}")

    args["working_directory"] = WORKING_DIR

    funct_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    func = funct_dict.get(func_name)

    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    function_result = func(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result}
            )
        ]
    )