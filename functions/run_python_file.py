import os, subprocess

def run_python_file(working_directory, file_path, args=[]):
    '''
    Function to run the python file. Returns the output and/or error message from running Python program.
    '''
    working_dir_abs = os.path.abspath(working_directory)
    target_file_abs = os.path.abspath(os.path.join(working_directory, file_path))

    # Check that the file is in the working directory
    if not target_file_abs.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if the file path exists
    if not os.path.exists(target_file_abs):
        return f'Error: File "{file_path}" not found.'
    
    # Check if file is a Python file
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    # Run the Python file
    try:
        # Create a list containing main command and args
        command = ["python3", file_path]
        if args:
            command.extend(args)
        
        # Run command
        completed_process = subprocess.run(
            command, 
            timeout=30,
            text=True, 
            capture_output=True, 
            cwd=working_dir_abs)

        # Extract output from CompletedProcess instance
        output = f'STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}'
        returncode = completed_process.returncode

        # Return message if there is no output
        if completed_process.stdout == None and completed_process.stderr == None:
            return 'No output produced'

        # Add on message in exit code is something other than 0
        if returncode == 0:
            return output
        else:
            return f"Process exited with code {returncode}\n" + output
        
    except Exception as e:
        return f'Error executing Python file: {e}'