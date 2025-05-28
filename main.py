from datetime import datetime
from dateutil import parser
import os
from pathlib import Path
import piexif
from PIL import Image

PATH_TO_FOLDER = ''

def input_target_folder():
    global PATH_TO_FOLDER
    cwd = os.getcwd()
    target_folder = input("Enter the name of the target folder: ")
    target_folder = target_folder.strip('./ ')
    PATH_TO_FOLDER = Path(cwd)/target_folder

    if os.path.exists(PATH_TO_FOLDER):
        print(f"\nPath to target folder: {PATH_TO_FOLDER}\n")
    else:
        print(f"\nFolder `{target_folder}` does not exist.\n")
    

class MyImage:
    
    DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
    
    def __init__(self, filename):
        self._filename: str = filename
        
    def __str__(self):
        return f"File {self._filename} has datetime '{self.dt}'"
        
    def _path_to_file(self):
        return str(PATH_TO_FOLDER/self._filename)
    
    def _exif_dict(self):
        path_to_file = self._path_to_file()
        return  piexif.load(path_to_file)
    
    @property
    def dt(self):
        exif_dict = self._exif_dict()
        return exif_dict['0th'].get(piexif.ImageIFD.DateTime)
        
    
    def _parse_image_datetime_from_filename(self):
        # Strip filename prefix and file extension
        filename_stripped = self._filename.lstrip('IMGPANO_-').rstrip('.jpg')
        # Format filename for parsing based on filename formatting
        if 'WA' in filename_stripped:
            filename_formatted = filename_stripped.split('-')[0]
        else:
            filename_formatted = filename_stripped.replace('_', ' ')
        # Parse formatted filename as datetime
        filename_parsed = parser.parse(filename_formatted)
        # Convert datetime into formatted string
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
    input_target_folder()
    files = os.listdir(PATH_TO_FOLDER)
    for filename in files:
        img = MyImage(filename)
        if img.dt:
            print(f"{filename} already has a datetime: {img.dt}")
        else:
            print(f"{filename} datetime is: {img.dt}")
            print("Insert datetime based on filename")
            img.set_datetime()
            print(f"{filename} datetime is now set to: {img.dt}")
            print("----------------------------------------------")
    
    
    

### TODO
# add print method str or dt
# pydantic: image validation
# handle error if not image
# implement setter to modify datetime into file
# Pylint
# print image file name
# move non-jpg to new folder