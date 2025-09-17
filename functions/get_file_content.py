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
    
    # Read from the file
    try:
        with open(target_file_abs, "r") as f:
            file_content_string = f.read(FILE_CHAR_LIMIT + 1)
        
        # Checks that file is actually longer than character limit, not just the exact limit
        is_truncated = len(file_content_string) > FILE_CHAR_LIMIT

        if is_truncated:
            # Revert content string back to char limit size
            file_content_string = file_content_string[:FILE_CHAR_LIMIT]

            # Add message if file is longer than set character limit
            file_content_string += f'[...File "{file_path}" truncated at {FILE_CHAR_LIMIT} characters]'

        return file_content_string
    except Exception as e:
        return f'Error reading file contents: {e}'