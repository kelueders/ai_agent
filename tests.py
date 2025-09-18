import re

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def general_tests():
    '''get_files_info() tests'''
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(result)

    '''get_file_content() tests'''
    # print('Result for "main.py":')
    # print(get_file_content("calculator", "main.py"))
    # print("")

    # print('Result for "pkg/calculator.py":')
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print("")
    
    # print('Result for "lorem.txt"')
    # print(get_file_content("calculator", "lorem.txt"))
    # print("")

    '''write_file() tests'''
    # print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    '''run_python_file() tests'''
    print('Result for "main.py":')
    print(run_python_file("calculator", "main.py"))
    print("")

    print('Result for "main.py", ["3 + 5"]')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("")

    print('Result for "tests.py"')
    print(run_python_file("calculator", "tests.py"))
    print("")

    print(run_python_file('calculator', '../main.py'))
    print(run_python_file('calculator', 'nonexistent.py'))

'''
PyTest Tests
'''
def test_get_files_bin():
    expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
    actual = get_files_info("calculator", "/bin")
    assert expected == actual

def test_get_files_parent():
    expected = 'Error: Cannot list "../" as it is outside the permitted working directory'
    actual = get_files_info("calculator", "../")
    assert expected == actual

def test_get_file_content_dir():
    expected = 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
    actual = get_file_content("calculator", "/bin/cat")
    assert expected == actual

def test_get_file_content_nonexist():
    expected = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    actual = get_file_content("calculator", "pkg/does_not_exist.py")
    assert expected == actual

def test_write_file_rewrite():
    expected = 'Successfully wrote to "lorem.txt" (28 characters written)'
    actual = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    assert expected == actual

def test_write_file_newfile():
    expected = 'Successfully wrote to "pkg/morelorem.txt" (26 characters written)'
    actual = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    assert expected == actual

def test_write_error():
    expected = 'Error: Cannot write to "/tmp/temp.txt" as it is outside the permitted working directory'
    actual = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    assert expected == actual

def test_run_file_wrong_dir():
    expected = 'Error: Cannot execute "../main.py" as it is outside the permitted working directory'
    actual = run_python_file("calculator", "../main.py")
    assert expected == actual

def test_run_file_nonexistent():
    expected = 'Error: File "nonexistent.py" not found.'
    actual = run_python_file("calculator", "nonexistent.py")
    assert expected == actual

if __name__ == "__main__":
    general_tests()