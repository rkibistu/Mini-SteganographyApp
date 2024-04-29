import piexif
from PIL import Image
import numpy as np

# VERY SIMPLE METHOD, EASY TO DETECT! -> should encrypt the message
# Encode message in binary and append it to the end of image file
def append_after(filename, message):
    with open(filename,"ab") as f:
        f.write(message.encode('utf8'))
# Extract message appended at the end of a JPG file        
def extract_append_after(filename):
    trailer = 'ffd9' # trailer for JPEG

    # Get trailer offset
    with open(filename, "rb") as cover_secret:
        file = cover_secret.read()
        offset = file.index(bytes.fromhex(trailer))

    # Write cover bytes to output file from offset + trailer length
    with open(filename, "rb") as cover_secret:
        cover_secret.seek(offset + len(trailer)//2)
        return cover_secret.read()
    
# Hides the secret in the image metadata (stored in the exif format): description
# (exif metadata is restricted in size and most paltforms will remove it on upload)
# More exif flags: https://github.com/hMatoba/Piexif/blob/master/piexif/_exif.py
#   piexif.ImageIFD.ImageDescription - change ImageDescription with anotehr tag 
#   to hide message on another place
def hide_inside_metadata(cover_filename, result_filename, message):
    im = Image.open(cover_filename)
    #check if exif dictionary is avaialble
    if "exif" in im.info:
        #load exif dictionary
        exif_dict = piexif.load(im.info["exif"])
        #modify the value of description from the dictionary
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = message
        #convert back to specific format
        exif_bytes = piexif.dump(exif_dict)
    else:
        #create a exif dictionary
        exif_bytes = piexif.dump({"0th":{piexif.ImageIFD.ImageDescription:message}})

    #write modified image
    im.save(result_filename, exif=exif_bytes)

def extract_from_metada(filename):
    im = Image.open(filename)
    result = piexif.load(im.info["exif"])["0th"][piexif.ImageIFD.ImageDescription].decode("utf-8")
    return result



