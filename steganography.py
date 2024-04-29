
# encod message in binary and append it to the end of image file
def append_after(filename, message):
    with open(filename,"ab") as f:
        f.write(message.encode('utf8'))
# extract message appended at the end of a JPG file        
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
    

          