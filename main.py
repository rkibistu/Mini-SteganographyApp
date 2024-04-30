import steganography as steg

import cv2

cover_img_path1 = "images/cover.jpg"
cover_img_path2 = "images/dog.png"
cover_img_path3 = "images/lsb_img1.jpg"
hidden_img_path = "images/lsb_img2.jpg"


def main():
    # steg.append_after(cover_img_path1,"My homeowrk here!")
    # test = steg.extract_append_after(cover_img_path)
    
    # steg.hide_inside_metadata(cover_img_path1,"images/metadata_secret.jpg","wuhuu, it is working!")
    # test = steg.extract_from_metada("images/metadata_secret.jpg")
    
    # steg.hide_message_inside_lsb(cover_img_path2,"images/lsb_msg_image.png","hello from lsb!")
    # test = steg.exctract_messge_from_lsb("images/lsb_msg_image.png",'!')
    # print(test)
    
    #steg.hide_image_inside_lsb(cover_img_path3,hidden_img_path,"images/hidden_img.png",2)
    #steg.extract_image_from_lsb("images/hidden_img.png","images/extracted_img1.png","images/extracted_img2.png",2)

    #steg.hide_message_inside_pallete(cover_img_path3, "culorile ascund ceva")
    
    #steg.dft(cover_img_path3, "images/dft.jpg")
    #steg.extract_message_dft("images/dft.jpg")

    dct_img = cv2.imread(cover_img_path3, cv2.IMREAD_UNCHANGED)
    dct_img_encoded = steg.DCT().encode_image(dct_img, "secreeet")
    cv2.imwrite("images/lasttest.png",dct_img_encoded)
    
    dct_img = cv2.imread("images/lasttest.png", cv2.IMREAD_UNCHANGED)
    dct_hidden_text = steg.DCT().decode_image(dct_img)
    print(dct_hidden_text)

if __name__ == "__main__":
    main()