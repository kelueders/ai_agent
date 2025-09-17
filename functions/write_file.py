import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        parent_dir = os.path.dirname(target_file_abs)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # if not os.path.exists(target_file_abs):
        #     with open(target_file_abs, "x") as f:
        #         f.write(content)
        # else:
        with open(target_file_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error writing to file: {e}"