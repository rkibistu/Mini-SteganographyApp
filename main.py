import steganography as steg
from tkinter import *
from customtkinter import *
import cv2
from PIL import Image

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

    # dct_img = cv2.imread(cover_img_path3, cv2.IMREAD_UNCHANGED)
    # dct_img_encoded = steg.DCT().encode_image(dct_img, "secreeet")
    # cv2.imwrite("images/lasttest.png",dct_img_encoded)
    
    # dct_img = cv2.imread("images/lasttest.png", cv2.IMREAD_UNCHANGED)
    # dct_hidden_text = steg.DCT().decode_image(dct_img)
    # print(dct_hidden_text)


def button_do_smth(label):
    image = PhotoImage(file="images/dog2.png")
    original_image = image.subsample(3,3)
    label.configure(image=original_image)
    label.image = original_image

def main():
    
    # tests()
    # exit(1)
    
    root = CTk()
    root.title("Steganography")
    root.configure(background="skyblue")

    # Create left and right frames
    left_frame = CTkFrame(root, width=400, height=600)
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = CTkFrame(root, width=850, height=600)
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # Create frames and labels in left_frame
    CTkLabel(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

    # load image to be "edited"
    image = Image.open(cover_img_path2)
    original_image = image.copy()
    image.thumbnail((100,100), Image.Resampling.LANCZOS)
    test = CTkLabel(left_frame, text='', image=CTkImage(dark_image=image, size=image.size))
    test.grid(row=1, column=0, padx=5, pady=5)

    # Display image in right_frame
    original_image.thumbnail((300,300), Image.Resampling.LANCZOS)
    print(original_image.size)
    CTkLabel(right_frame,text='', image=CTkImage(dark_image=original_image, size=original_image.size)).grid(row=0,column=0, padx=5, pady=5)

    # Create tool bar frame
    tool_bar = CTkFrame(left_frame, width=180, height=185)
    tool_bar.grid(row=2, column=0, padx=5, pady=5)

    # Example labels that serve as placeholders for other widgets
    CTkButton(tool_bar, text="Tools", command=lambda:open_extract_secret_message_window(root)).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
    CTkButton(tool_bar, text="Filters", command=lambda:open_hide_secret_message_window(root)).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

    # Example labels that could be displayed under the "Tool" menu
    CTkButton(tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)
    CTkLabel(tool_bar, text="Crop").grid(row=2, column=0, padx=5, pady=5)
    CTkLabel(tool_bar, text="Rotate & Flip").grid(row=3, column=0, padx=5, pady=5)
    CTkLabel(tool_bar, text="Resize").grid(row=4, column=0, padx=5, pady=5)
    CTkLabel(tool_bar, text="Exposure").grid(row=5, column=0, padx=5, pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()