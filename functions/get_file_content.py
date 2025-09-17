import os

from config import FILE_CHAR_LIMIT

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))

    # Check that the file is in the working directory
    if not target_file_abs.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    # Confirm the file is a file and that it exists
    if not os.path.isfile(target_file_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        # Read from the file
        with open(target_file_abs, "r") as f:
            file_content_string = f.read(FILE_CHAR_LIMIT)

        if len(file_content_string) == FILE_CHAR_LIMIT:
            file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f'Error reading file contents: {e}'