import os

def get_files_info(working_directory, directory="."):
    '''
    List the contents of a directory and view the file/directory metadata (name and size)
    '''
    # Get full path names for files
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # If the target path is outside the working directory, then return an error
    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # If the target path is not a directory, return an error
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    # Create list of files in target directory with info on file size and whether or not it is a directory
    try:
        contents = os.listdir(full_path)
        contents_arr = []
        for file in contents:
            size = 0

            # Combine full target path with file
            file_path = os.path.join(full_path, file)

            # Get file information
            size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            # Format information into string
            file_info = f'- {file}: file_size={size} bytes, is_dir={is_dir}'
            contents_arr.append(file_info)

        return "\n".join(contents_arr)
    
    # If there is a problem with file information, return an error
    except Exception as e:
        return f'Error listing file information: {e}'

