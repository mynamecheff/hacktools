import sys
import os

class SignFile:
    def __init__(self, sign, suffix_file, file_format):
        self.sign = sign
        self.suffix_file = suffix_file
        self.file_format = file_format

def main():
    if len(sys.argv) == 1:
        print(f"Use: {sys.argv[0]} fileUnknown fileUnknown fileUnknown ...")
    else:
        mass_sign = [
            SignFile("474946", "*.gif", "GIF files"),
            SignFile("GIF89a", "*.gif", "GIF files"),
            SignFile("FFD8FF", "*.jpg", "JPEG files"),
            SignFile("JFIF", "*.jpg", "JPEG files"),
            SignFile("504B03", "*.zip", "ZIP files"),
            # ... Add other entries as needed
        ]

        for file in sys.argv[1:]:
            try:
                with open(file, "rb") as f:
                    content = f.read()
                    for val in mass_sign:
                        if file.endswith(val.suffix_file) or val.sign.encode() in content:
                            print(f"{file} may be {val.file_format}")
                            break
            except Exception as e:
                print(f"{file}: {e}")

if __name__ == "__main__":
    main()
