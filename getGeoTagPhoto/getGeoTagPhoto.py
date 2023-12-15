from PIL import Image
from PIL.ExifTags import TAGS
import sys

def get_exif_data(file_path):
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                decoded_exif = {TAGS[key]: exif_data[key] for key in exif_data.keys() if key in TAGS and exif_data[key] is not None}
                return decoded_exif
            else:
                return {}
    except Exception as e:
        print(f"Error while extracting EXIF data: {e}")
        return {}

def main():
    if len(sys.argv) == 1:
        print(f"Use: {sys.argv[0]} photo")
    else:
        file_path = sys.argv[1]
        exif_data = get_exif_data(file_path)

        if exif_data:
            latitude = exif_data.get('GPSInfo', {}).get(2)
            longitude = exif_data.get('GPSInfo', {}).get(4)

            if latitude is not None and longitude is not None:
                print(f"{file_path}\nlat:\t{latitude}\nlong:\t{longitude}")
            else:
                print(f"No GPS coordinates found in {file_path}")
        else:
            print(f"No EXIF data found in {file_path}")

if __name__ == "__main__":
    main()
