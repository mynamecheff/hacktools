import os
import sys
import time

def main():
    if len(sys.argv) == 1:
        print(f"Using: {sys.argv[0]} file")
        sys.exit(1)

    file_path = sys.argv[1]

    try:
        file_info = os.stat(file_path)
    except FileNotFoundError:
        print("File does not exist.")
        sys.exit(1)

    print("File name:", os.path.basename(file_path))
    print("Size in bytes:", file_info.st_size)
    print("Permissions:", oct(file_info.st_mode & 0o777))
    print("Last modified:", time.ctime(file_info.st_mtime))
    print("Is Directory:", os.path.isdir(file_path))
    print("System info:", file_info)

if __name__ == "__main__":
    main()
