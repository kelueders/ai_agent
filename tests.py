import re

from functions.get_files_info import get_files_info

def general_tests():
    result = get_files_info("calculator", ".")
    print("Result for current directory:")
    print(result)
    print("")

    result = get_files_info("calculator", "pkg")
    print("Result for 'pkg' directory:")
    print(result)

def test_get_files_bin():
    expected = 'Error: Cannot list "/bin" as it is outside the permitted working directory'
    actual = get_files_info("calculator", "/bin")
    assert expected == actual

def test_get_files_parent():
    expected = 'Error: Cannot list "../" as it is outside the permitted working directory'
    actual = get_files_info("calculator", "../")
    assert expected == actual

if __name__ == "__main__":
    general_tests()