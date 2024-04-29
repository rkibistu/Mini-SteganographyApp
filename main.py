import steganography as steg

cover_img_path1 = "images/cover.jpg"
cover_img_path2 = "images/dog.png"


def main():
    # steg.append_after(cover_img_path1,"My homeowrk here!")
    # test = steg.extract_append_after(cover_img_path)
    
    # steg.hide_inside_metadata(cover_img_path1,"images/metadata_secret.jpg","wuhuu, it is working!")
    # test = steg.extract_from_metada("images/metadata_secret.jpg")
    
    steg.hide_message_inside_lsb(cover_img_path2,"images/lsb_msg_image.png","hello from lsb!")
    test = steg.exctract_messge_from_lsb("images/lsb_msg_image.png",'!')
    print(test)

if __name__ == "__main__":
    main()