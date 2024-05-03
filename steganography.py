import piexif
from PIL import Image
import numpy as np
import cv2 
import random
from Pylette import extract_colors
from scipy.fftpack import dct, idct
import itertools
from pathlib import Path

temp_image_name = 'temp/temp.png'

def check_file_extension(filename, extension):
    return Path(filename).suffix.lower() == extension.lower()

# VERY SIMPLE METHOD, EASY TO DETECT! -> should encrypt the message
# Encode message in binary and append it to the end of image file
def append_after(filename,result_filename,message):
    temp_img = cv2.imread(filename)
    cv2.imwrite(result_filename,temp_img)
    with open(result_filename,"ab") as f:
        f.write(message.encode('utf8'))
    return result_filename
# Extract message appended at the end of a JPG file        
def extract_append_after(filename):
    trailer = ''
    if(check_file_extension(filename,".jpg")):
        trailer = 'ffd9' # trailer for JPEG
    if(check_file_extension(filename,".png")):
        trailer = '49454E44' # trailer for PNG

    # Get trailer offset
    with open(filename, "rb") as cover_secret:
        file = cover_secret.read()
        offset = file.index(bytes.fromhex(trailer))
    
    if(check_file_extension(filename,".png")):
        offset+=4 #only for png

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

    channels = 0
    # Get the image pixel arrays 
    with Image.open(filename) as img:
        width, height = img.size
        data = np.array(img)
        channels = len(img.mode)
        if(img.mode == 'P'):
            print("Image written in pallete mode not supported!")
            return -1

        
    # Flatten the pixel arrays (only one array)
    data = np.reshape(data, width*height*channels)

    # Overwrite pixel LSB
    data[:b_message_lenght] = data[:b_message_lenght] & ~1 | b_message

    # Reshape back to an image pixel array
    data = np.reshape(data, (height, width, channels))

    new_img = Image.fromarray(data)
    new_img.save(result_filename)
    
    return 1

# end_of_message is the character that marsk the end of the message
#   if not present, read until see an unprintable value
def exctract_messge_from_lsb(filename, end_of_message = None):
    channels = 0
    with Image.open(filename) as img:
        width, height = img.size
         # Get the image pixel arrays 
        data = np.array(img)
        channels = len(img.mode)
    
    # Flatten the pixel arrays (only one array)
    data = np.reshape(data, width*height*channels)
    
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
    
    # img1 and img2 are two blank images 
    img1 = np.zeros((height, width, 3), np.uint8) 
    img2 = np.zeros((height, width, 3), np.uint8) 
      
    for i in range(height ): 
        for j in range(width): 
            for l in range(3): 
                v1 = format(img[i][j][l], '08b') 
                v2 = v1[:(8-bits_no)] + chr(random.randint(0, 1)+48) * bits_no
                v3 = v1[(8-bits_no):] + chr(random.randint(0, 1)+48) * (8-bits_no)
                  
                # Appending data to img1 and img2 
                img1[i][j][l]= int(v2, 2) 
                img2[i][j][l]= int(v3, 2) 
      
    # These are two images produced from 
    # the encrypted image 
    cv2.imwrite(result_cover_path, img1) 
    cv2.imwrite(result_hidden_path, img2) 
    

# hide info inside color pallete
def hide_message_inside_pallete(filename, message):
    palette = extract_colors(filename, palette_size=20, resize=True)
    
    print(palette[0].rgb)
    
    palette[0].rgb = (29,13,15)
    print(palette[0].rgb)
    
    palette.display(save_to_file=False)
    
    print(type(palette))
    
 
def dft(filename, result_filename):
    message = "secret"

    data = np.array([ord(char) for char in message])
    data = np.append(data, [0, 0, 0, 0])

    im = np.array(Image.open(filename))

    red = im[:, :, 0]
    arr = np.fft.fft2(red)
    compl = np.imag(arr)
    arr = np.real(arr)
    r, c = arr.shape

    data_index = 0
    for i in range(r-1, -1, -1):
        for j in range(c-1, -1, -1):
            if data_index < len(data):
                arr[i, j] = data[data_index]
                print(i,j)
                data_index += 1
            else:
                break

    newfftred = arr + 1j * compl
    newred = np.real(np.fft.ifft2(newfftred))
    
    print(red[0][0])
    print(newfftred[0][0])
    
    newim = np.copy(im)
    newim[:, :, 0] = newred
    
    new_img = Image.fromarray(newim)
    new_img.save(result_filename) 
def extract_message_dft(filename):

    message = "secret"

    data = np.array([ord(char) for char in message])
    data = np.append(data, [0, 0, 0, 0])

    im = np.array(Image.open(filename))

    newred = im[:, :, 0]
    
    
    arr = np.fft.fft2(newred)
    compl = np.imag(arr)
    arr = np.real(arr)
    
    newfftred = arr + 1j * compl
    
    print(newred[0][0])
    print(newfftred[0][0])
   

# hide info inside DCT coefficients
quant = np.array([[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

#encoding part : 
def hide_message_inside_dct(filename_path, result_path,secret_msg):
    #show(img)
    img = cv2.imread(filename_path, cv2.IMREAD_UNCHANGED)
    w,h,channels = img.shape
    if(channels != 3):
        print("Wrong fromat. Expected 3 channels image, got: ",channels)
        return -1
    secret=secret_msg
    message = str(len(secret))+'*'+secret
    bitMess = toBits(message)
    #get size of image in pixels
    row,col = img.shape[:2]
    ##col, row = img.size
    oriRow, oriCol = row, col  
    if((col/8)*(row/8)<len(secret)):
        print("Error: Message too large to encode in image")
        return False
    #make divisible by 8x8
    if row%8 != 0 or col%8 != 0:
        img = addPadd(img, row, col)
    
    row,col = img.shape[:2]
    ##col, row = img.size
    #split image into RGB channels
    bImg,gImg,rImg = cv2.split(img)
    #message to be hid in blue channel so converted to type float32 for dct function
    bImg = np.float32(bImg)
    #break into 8x8 blocks
    imgBlocks = [np.round(bImg[j:j+8, i:i+8]-128) for (j,i) in itertools.product(range(0,row,8),
                                                                    range(0,col,8))]
    #Blocks are run through DCT function
    dctBlocks = [np.round(cv2.dct(img_Block)) for img_Block in imgBlocks]
    #blocks then run through quantization table
    quantizedDCT = [np.round(dct_Block/quant) for dct_Block in dctBlocks]
    #set LSB in DC value corresponding bit of message
    messIndex = 0
    letterIndex = 0
    for quantizedBlock in quantizedDCT:
        #find LSB in DC coeff and replace with message bit
        DC = quantizedBlock[0][0]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        DC[7] = bitMess[messIndex][letterIndex]
        DC = np.packbits(DC)
        DC = np.float32(DC)
        DC= DC-255
        quantizedBlock[0][0] = DC
        letterIndex = letterIndex+1
        if letterIndex == 8:
            letterIndex = 0
            messIndex = messIndex + 1
            if messIndex == len(message):
                break
    #blocks run inversely through quantization table
    sImgBlocks = [quantizedBlock *quant+128 for quantizedBlock in quantizedDCT]
    #puts the new image back together
    sImg=[]
    for chunkRowBlocks in chunks(sImgBlocks, col/8):
        for rowBlockNum in range(8):
            for block in chunkRowBlocks:
                sImg.extend(block[rowBlockNum])
    sImg = np.array(sImg).reshape(row, col)
    #converted from type float32
    sImg = np.uint8(sImg)
    #show(sImg)
    sImg = cv2.merge((sImg,gImg,rImg))
    cv2.imwrite(result_path,sImg)
    return result_path

#decoding part :
def extract_message_from_dct(filename):
    result = ''
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    row,col = img.shape[:2]
    messSize = None
    messageBits = []
    buff = 0
    #split image into RGB channels
    bImg,gImg,rImg = cv2.split(img)
        #message hid in blue channel so converted to type float32 for dct function
    bImg = np.float32(bImg)
    #break into 8x8 blocks
    imgBlocks = [bImg[j:j+8, i:i+8]-128 for (j,i) in itertools.product(range(0,row,8),
                                                                    range(0,col,8))]    
    #blocks run through quantization table
    #quantizedDCT = [dct_Block/ (quant) for dct_Block in dctBlocks]
    quantizedDCT = [img_Block/quant for img_Block in imgBlocks]
    i=0
    #message extracted from LSB of DC coeff
    for quantizedBlock in quantizedDCT:
        DC = quantizedBlock[0][0]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        if DC[7] == 1:
            buff+=(0 & 1) << (7-i)
        elif DC[7] == 0:
            buff+=(1&1) << (7-i)
        i=1+i
        if i == 8:
            messageBits.append(chr(buff))
            buff = 0
            i =0
            if messageBits[-1] == '*' and messSize is None:
                try:
                    messSize = int(''.join(messageBits[:-1]))
                except:
                    pass
        if len(messageBits) - len(str(messSize)) - 1 == messSize:
            return ''.join(messageBits)[len(str(messSize))+1:]
    return ''
      
"""Helper function to 'stitch' new image back together"""
def chunks(l, n):
    m = int(n)
    for i in range(0, len(l), m):
        yield l[i:i + m]
def addPadd(img, row, col):
    img = cv2.resize(img,(col+(8-col%8),row+(8-row%8)))    
    return img
def toBits(message):
    bits = []
    for char in message:
        binval = bin(ord(char))[2:].rjust(8,'0')
        bits.append(binval)
    numBits = bin(len(bits))[2:].rjust(8,'0')
    return bits


def bitplanes(filename, result_filename):
    img = Image.open(filename).convert('L')
    data = np.array(img)
    out = []
    # create an image for each k bit plane
    for k in range(7,-1,-1):
    # extract kth bit (from 0 to 7)
        res = data // 2**k & 1
        out.append(res*255)
    # stack generated images
    b = np.hstack(out)
    result =  Image.fromarray(b)
    result.save(result_filename)
    return result

def bitplanes2(filename, result_filename):
    img = Image.open(filename)
    data = np.array(img)
    out = []

    if len(data.shape) == 3:  # RGB image
        height, width, channels = data.shape
        for channel in range(channels):
            channel_data = data[:, :, channel]
            channel_out = []
            for k in range(7, -1, -1):
                res = channel_data // 2**k & 1
                channel_out.append(res * 255)
            out.append(np.hstack(channel_out))
        result = Image.fromarray(np.stack(out, axis=-1).astype(np.uint8))
    else:  # Grayscale image
        for k in range(7, -1, -1):
            res = data // 2**k & 1
            out.append(res * 255)
        result = Image.fromarray(np.hstack(out).astype(np.uint8))

    result.save(result_filename)
    return result