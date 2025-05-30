from datetime import datetime
from dateutil import parser
import magic
import os
from pathlib import Path
import piexif
from PIL import Image

PATH_TO_FOLDER: str = Path('./assets')
        
def validate_jpeg(filename: str) -> bool:
    mime_type = magic.from_file(filename, mime=True)
    if mime_type == 'image/jpeg':
        print(f"File: {filename}. MIME type:{mime_type}")
        return True
    else:
        print(f"File: {filename}. MIME type:{mime_type}")
        return False

class MyImage:
    
    DATETIME_FORMAT: str = "%Y:%m:%d %H:%M:%S"
    
    def __init__(self, filename: str):
        self._filename: str = filename
        
    def _path_to_file(self) -> str:
        return str(PATH_TO_FOLDER/self._filename)
    
    def _exif_dict(self) -> dict:
        path_to_file: str = self._path_to_file()
        return  piexif.load(path_to_file)
    
    @property
    def dt(self) -> bytes:
        exif_dict: dict = self._exif_dict()
        return exif_dict['0th'].get(piexif.ImageIFD.DateTime)
    
    def _parse_image_datetime_from_filename(self) -> str:
        # Strip filename prefix and file extension
        filename_stripped: str = self._filename.lstrip('IMGPANO_-').rstrip('.jpg')
        # Format filename for parsing based on filename formatting
        if 'WA' in filename_stripped:
            filename_formatted: str = filename_stripped.split('-')[0]
        else:
            filename_formatted: str = filename_stripped.replace('_', ' ')
        # Parse formatted filename as datetime
        filename_parsed: datetime = parser.parse(filename_formatted)
        # Convert datetime into formatted string
        file_datetime: str = filename_parsed.strftime(self.DATETIME_FORMAT)
        return file_datetime
    
    def set_datetime(self) -> None:
        file_datetime: str = self._parse_image_datetime_from_filename()
        self._exif_dict['0th'][piexif.ImageIFD.DateTime] = file_datetime
        exif_bytes: bytes = piexif.dump(self._exif_dict)  # Convert properties into bytes
        piexif.insert(exif_bytes, self._path_to_file)

    def show_image(self) -> None:
        with Image.open(self._path_to_file) as img:
            img.show()
    
    def __str__(self):
        return f"{self._filename}"

if __name__ == '__main__':
    for file in os.listdir(PATH_TO_FOLDER):
        if validate_jpeg(PATH_TO_FOLDER/file):
            img = MyImage(file)
            if img.dt:
                print(f"{file} already has a datetime: {img.dt}")
            else:
                print(f"{file} datetime is: {img.dt}")
                print("Insert datetime based on filename")
                img.set_datetime()
                print(f"{file} datetime is now set to: {img.dt}")
                print("----------------------------------------------")
                