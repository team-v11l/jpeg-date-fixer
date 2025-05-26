from datetime import datetime
from dateutil import parser
import os
from pathlib import Path
import piexif
from PIL import Image


class MyImage:
    
    DIRECTORY = Path('./images')
    DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
    
    def __init__(self, filename):
        self._filename: str = filename
        self._path_to_file = str(self.DIRECTORY/filename)
        self._exif_dict: dict = piexif.load(self._path_to_file)
    
    @property
    def dt(self):
        return self._exif_dict['0th'].get(piexif.ImageIFD.DateTime)
        
    def _parse_image_datetime_from_filename(self):
        # Strip filename prefix and file extension
        filename_stripped = self._filename.lstrip('IMGPANO_-').rstrip('.jpg')
        # Format filename for parsing based on filename formatting
        if 'WA' in filename_stripped:
            filename_formatted = filename_stripped.split('-')[0]
        else:
            filename_formatted = filename_stripped.replace('_', ' ')
        # Parse and cast formatted filename as datetime
        filename_parsed = parser.parse(filename_formatted)
        # Cast datetime as string
        file_datetime = filename_parsed.strftime(self.DATETIME_FORMAT)
        return file_datetime
    
    def set_datetime(self):
        file_datetime = self._parse_image_datetime_from_filename()
        self._exif_dict['0th'][piexif.ImageIFD.DateTime] = file_datetime
        exif_bytes = piexif.dump(self._exif_dict)  # Convert properties into bytes
        piexif.insert(exif_bytes, self._path_to_file)

    def show_image(self):
        with Image.open(self._path_to_file) as img:
            img.show()


if __name__ == '__main__':
    files = os.listdir(MyImage.DIRECTORY)
    for filename in files:
        img = MyImage(filename)
        if img.dt:
            print(f"{filename} already has a datetime: {img.dt}")
        else:
            print(f"{filename} datetime is: {img.dt}")
            print("Insert datetime based on filename")
            img.set_datetime()
            print(f"{filename} datetime is now set to: {img.dt}")
    
    
    

### TODO
# add print method str or dt
# pydantic: image validation
# handle error if not image
# implement setter to modify datetime into file
# Pylint