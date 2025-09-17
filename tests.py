import re

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

def general_tests():
#     result = get_files_info("calculator", ".")
#     print("Result for current directory:")
#     print(result)
#     print("")

#     result = get_files_info("calculator", "pkg")
#     print("Result for 'pkg' directory:")
#     print(result)

    print('Result for "main.py":')
    print(get_file_content("calculator", "main.py"))
    print("")

    print('Result for "pkg/calculator.py":')
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("")
    
    # print('Result for "lorem.txt"')
    # print(get_file_content("calculator", "lorem.txt"))
    # print("")

# def test_get_files_bin():
#     expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
#     actual = get_files_info("calculator", "/bin")
#     assert expected == actual

# def test_get_files_parent():
#     expected = 'Error: Cannot list "../" as it is outside the permitted working directory'
#     actual = get_files_info("calculator", "../")
#     assert expected == actual

def test_get_file_content_dir():
    expected = 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory'
    actual = get_file_content("calculator", "/bin/cat")
    assert expected == actual

def test_get_file_content_nonexist():
    expected = 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"'
    actual = get_file_content("calculator", "pkg/does_not_exist.py")
    assert expected == actual


if __name__ == "__main__":
    general_tests()