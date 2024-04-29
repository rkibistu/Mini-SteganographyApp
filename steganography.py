import piexif
from PIL import Image
import numpy as np
import cv2 
import random

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



# Hide message inside LSB of the image
# JPG is problematic with this because LSB may be lost during compression.
#   use: png, gif, bitmap
def hide_message_inside_lsb(filename, result_filename, message, end_of_message = None):
    
    # add a character to amrk end of message
    if(end_of_message != None):
        message += end_of_message
    
    # Encode the message in a serie of 8-bit values (covnert to binary)
    b_message = ''.join(["{:08b}".format(ord(x)) for x in message ])
    b_message = [int(x) for x in b_message]

    b_message_lenght = len(b_message)

    # Get the image pixel arrays 
    with Image.open(filename) as img:
        width, height = img.size
        data = np.array(img)
        
    # Flatten the pixel arrays (only one array)
    data = np.reshape(data, width*height*4)

    # Overwrite pixel LSB
    data[:b_message_lenght] = data[:b_message_lenght] & ~1 | b_message

    # Reshape back to an image pixel array
    data = np.reshape(data, (height, width, 4))

    new_img = Image.fromarray(data)
    new_img.save(result_filename)

# end_of_message is the character that marsk the end of the message
#   if not present, read until see an unprintable value
def exctract_messge_from_lsb(filename, end_of_message = None):
    with Image.open(filename) as img:
        width, height = img.size
         # Get the image pixel arrays 
        data = np.array(img)
    
    # Flatten the pixel arrays (only one array)
    data = np.reshape(data, width*height*4)
    
    # extract lsb
    data = data & 1 
    
    # Packs binary-valued array into 8-bits array.
    data = np.packbits(data)
    
    # Read and convert integer to Unicode characters until hitting a non-printable character
    result = ''
    for x in data:
        l = chr(x)
        if(end_of_message != None and l == end_of_message):
            break
        elif not l.isprintable():
            break
        result += l
    return result

# hide another image inside an image using bits_no of bits for the hidden imageg
def hide_image_inside_lsb(cover_image_path, secret_image_path, result_image_path, bits_no=4):
    img1 = cv2.imread(cover_image_path) 
    img2 = cv2.imread(secret_image_path) 
    
    print(img1.shape)

      
    for i in range(img2.shape[0]): 
        for j in range(img2.shape[1]): 
            for l in range(3): 
                  
                # v1 and v2 are 8-bit pixel values 
                # of img1 and img2 respectively 
                v1 = format(img1[i][j][l], '08b') 
                v2 = format(img2[i][j][l], '08b') 
                  
                # Taking 4 MSBs of each image 
                v3 = v1[:(8-bits_no)] + v2[:bits_no]  
                  
                img1[i][j][l]= int(v3, 2) 
                  
    cv2.imwrite(result_image_path, img1)
    
def extract_image_from_lsb(image_path, result_cover_path, result_hidden_path, bits_no = 4):

    img = cv2.imread(image_path)  
    height = img.shape[0] 
    width = img.shape[1] 
    
    print(width)
    print(height)
    
      
    # img1 and img2 are two blank images 
    img1 = np.zeros((height, width, 3), np.uint8) 
    img2 = np.zeros((height, width, 3), np.uint8) 
      
    for i in range(height ): 
        for j in range(width): 
            for l in range(3): 
                v1 = format(img[i][j][l], '08b') 
                v2 = v1[:(8-bits_no)] + chr(random.randint(0, 1)+48) * bits_no
                v3 = v1[bits_no:] + chr(random.randint(0, 1)+48) * (8-bits_no)
                  
                # Appending data to img1 and img2 
                img1[i][j][l]= int(v2, 2) 
                img2[i][j][l]= int(v3, 2) 
      
    # These are two images produced from 
    # the encrypted image 
    cv2.imwrite(result_cover_path, img1) 
    cv2.imwrite(result_hidden_path, img2) 