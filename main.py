import steganography as steg
from tkinter import *
from customtkinter import *
import cv2
from PIL import Image

from GUI.main_window import open_main_window
from GUI.hide_secret_image_window import open_hide_secret_message_window
from GUI.extract_secret_image_window import open_extract_secret_message_window

cover_img_path1 = "images/cover.jpg"
cover_img_path2 = "images/dog.png"
cover_img_path3 = "images/lsb_img1.jpg"
hidden_img_path = "images/lsb_img2.jpg"

def tests():
    # steg.append_after(cover_img_path2,"My homeowrk here!")
    test = steg.extract_append_after("temp/temp.png")
    print(test)
    
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

    steg.hide_message_inside_dct(cover_img_path3,"images/lasttest.png", "secreeet")
    
    dct_hidden_text = steg.extract_message_from_dct("images/lasttest.png")
    print(dct_hidden_text)

def button_do_smth(label):
    image = PhotoImage(file="images/dog2.png")
    original_image = image.subsample(3,3)
    label.configure(image=original_image)
    label.image = original_image

def main():
    
    tests()
    # exit(1)
    # open_main_window()
    

if __name__ == "__main__":
    main()