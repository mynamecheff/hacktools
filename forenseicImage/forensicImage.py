from PIL import Image
import sys

def main():
    if len(sys.argv) == 1:
        print(f"Use: {sys.argv[0]} fileUnknown fileUnknown fileUnknown ...")
    else:
        for file in sys.argv[1:]:
            try:
                with open(file, "rb") as f:
                    img = Image.open(f)
                    print(f"{file} Format = {img.format}")
            except Exception as e:
                print(f"{file}: {e}")

if __name__ == "__main__":
    main()
