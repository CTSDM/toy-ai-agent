from functions.run_python_file import run_python_file


def main():
    working_dirs = [
        "calculator",
        "calculator",
        "calculator",
        "calculator",
        "calculator",
    ]
    dirs = ["main.py", "main.py", "tests.py", "../main.py", "nonexistent.py"]
    contents = [None, ["3 + 5"], None, None, None]
    for i in range(len(working_dirs)):
        print(f"Result for {dirs[i]} directory:")
        if contents[i]:
            print(run_python_file(working_dirs[i], dirs[i], contents[i]))
        else:
            print(run_python_file(working_dirs[i], dirs[i]))


if __name__ == "__main__":
    main()
