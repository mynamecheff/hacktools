import fitz  # PyMuPDF

def print_meta(filename):
    try:
        # Open the PDF file
        pdf_document = fitz.open(filename)

        # Get metadata information
        metadata = pdf_document.metadata
        info_dict = metadata.items()

        # Print metadata information
        for key, value in info_dict:
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")

def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print(f"Use: {sys.argv[0]} FILE.pdf")
        sys.exit(1)

    # Call the function to print metadata
    print_meta(sys.argv[1])

if __name__ == "__main__":
    main()
