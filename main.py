import steganography as steg

cover_img_path = "images/cover.jpg"


def main():
    # steg.append_after(cover_img_path,"My homeowrk here!")
    # test = steg.extract_append_after(cover_img_path)
    
    steg.hide_inside_metadata(cover_img_path,"images/metadata_secret.jpg","wuhuu, it is working!")
    test = steg.extract_from_metada("images/metadata_secret.jpg")
    print(test)

if __name__ == "__main__":
    main()