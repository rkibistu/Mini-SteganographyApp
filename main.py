import steganography as steg

cover_img_path = "images/cover.jpg"

def main():
    steg.append_after(cover_img_path,"My homeowrk here!")
    test = steg.extract_append_after(cover_img_path)
    print(test)

if __name__ == "__main__":
    main()