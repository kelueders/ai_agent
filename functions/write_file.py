import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))

    # Make sure target file is in the working directory
    if not target_file_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    # Check if the absolute file_path exists, if not make the necessary parent directories
    if not os.path.exists(target_file_abs):
        try:
            parent_dir = os.path.dirname(target_file_abs)
            if not os.path.exists(parent_dir):
                os.makedirs(parent_dir)
        except Exception as e:
            return f"Error creating directory: {e}"
    
    # If the file_path exists, but it's a directory, return an error
    if os.path.exists(target_file_abs) and os.path.isdir(target_file_abs):
        return f'Error: "{file_path} is a directory, not a file'

    # Write to the file, creating a new one if it doesn't exist already
    try:
        with open(target_file_abs, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'  
    except Exception as e:
        return f"Error writing to file: {e}"