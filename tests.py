from functions.get_file_content import get_file_content


def main():
    working_dirs = ["calculator", "calculator", "calculator", "calculator"]
    dirs = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]
    for i in range(len(working_dirs)):
        print(f"Result for {dirs[i]} directory:")
        print(get_file_content(working_dirs[i], dirs[i]))


if __name__ == "__main__":
    main()
