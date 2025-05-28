# JPEG Date Fixer
## Description
JPEG Date Fixer is a Python application designed to manage and correct the `DateTime` metadata of JPEG image files. It extracts the date and time information from the filenames of images and updates the EXIF metadata accordingly. This is particularly useful for organizing images where the metadata is missing or incorrect.

## Filename Format
The application expects filenames to follow specific patterns to extract date and time information. Examples of supported formats:

- **WhatsApp Images**: IMG-YYYYMMDD-WAXXXX.jpg (e.g. IMG-20180120-WA0004.jpg)
- **Phone Camera Images**: IMG_YYYYMMDD_HHMMSS.jpg (e.g. IMG_20250124_235316.jpg)

## Next steps
- Add data validation i.e. input file is a JPEG image
- Create log file
- Containerise the app
- Finalise README