from customtkinter import *
from PIL import Image

from GUI.hide_secret_image_window import open_hide_secret_message_window
from GUI.extract_secret_image_window import open_extract_secret_message_window
from GUI.lsb_images_window import open_lsb_images_window

def open_main_window():
    root = CTk()
    root.title("Steganography")
    root.configure(background="skyblue")

    # Example labels that serve as placeholders for other widgets
    CTkButton(root, text="Extract message", command=lambda:open_extract_secret_message_window(root)).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
    CTkButton(root, text="Hide message", command=lambda:open_hide_secret_message_window(root)).grid(row=1, column=0, padx=5, pady=3, ipadx=10)
    CTkButton(root, text="Hide image", command=lambda:open_lsb_images_window(root)).grid(row=2, column=0, padx=5, pady=3, ipadx=10)

 
    root.mainloop()