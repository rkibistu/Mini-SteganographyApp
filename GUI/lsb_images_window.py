from customtkinter import *
from customtkinter import filedialog
import steganography as steg
import shutil
import os
from PIL import Image
from GUI.settings import * 

default_loaded_image = 'images/question.png'
loaded_source_image = default_loaded_image
loaded_dest_image = default_loaded_image
loaded_result_image = default_loaded_image

def slider_event(value):
    print(value)
    
def sel():
   selection = "You selected the option " + str(var.get())
   label.config(text = selection)
    
def browseFiles(image_label, mode):
    global loaded_source_image
    global loaded_dest_image
    global loaded_result_image
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("PNG files",
                                                        "*.png")
                                                        ,("all files",
                                                        "*.*")))
    if(filename == ''):
        return 
      
    # Change label contents
    loaded_image_path = filename 
    new_image = Image.open(loaded_image_path)
    new_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT)) 
    image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
    image_label.image = CTkImage(dark_image=new_image,size=new_image.size)
    
    #update global path
    if(mode == 'src'):
        loaded_source_image = loaded_image_path
    elif(mode == 'dest'):
        loaded_dest_image = loaded_image_path
    elif(mode == 'result'):
        loaded_result_image = loaded_image_path
    else:
        print("Wrong mode: ",mode)

def open_lsb_images_window(root_window):
    #reset to default settings everytime it opens
    global loaded_source_image
    global loaded_dest_image
    global loaded_result_image
    loaded_source_image = default_loaded_image
    loaded_dest_image = default_loaded_image
    loaded_result_image = default_loaded_image


    window = CTkToplevel(root_window)
    window.title("Image inside image")
    window.configure(background="skyblue")
    window.grab_set()

    # Create left and right frames
    left_frame = CTkFrame(window, width=400, height=600)
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = CTkFrame(window, width=850, height=600)
    right_frame.grid(row=0, column=1, padx=10, pady=5)
    
    #left frame
    CTkLabel(left_frame, text = "Direction").grid(row=0,column = 0,padx=5, pady=5)
    #add radio button here
    
    #add methids
    
    #add plane bits image
    
    # Create tool bar frame
    tool_bar = CTkFrame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    
    secret_message_entry = CTkEntry(tool_bar)
    CTkLabel(tool_bar, text="Secret:").grid(row=0, column=0, padx=5, pady=3, ipadx=10) 
    secret_message_entry.grid(row=0, column=1, padx=5, pady=3, ipadx=10, sticky='ew') 

    # Example labels that serve as placeholders for other widgets
    CTkLabel(tool_bar, text="METHODS:").grid(row=3, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=2) 

    # Example labels that could be displayed under the "Tool" menu
    CTkButton(tool_bar, text="Basic LSB" ).grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="XOR").grid(row=5, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    
    # Display objects in right_frame
    CTkLabel(right_frame,text='Lets\' hide some images').grid(row=0,column=0, padx=5, pady=5, sticky='new', columnspan=10)
    CTkLabel(right_frame,text='Bits for secret:').grid(row=1,column=0, padx=5, pady=5, sticky='new', columnspan=10)
    bitsSlider = CTkSlider(master=right_frame, from_=1, to=8, command=slider_event, number_of_steps=7)
    bitsSlider.grid(row=2,column=0, padx=5, pady=5, sticky='ew', columnspan=10)
    
    # 3 images
    source_image = Image.open(loaded_source_image)
    source_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT))
    source_image_label = CTkLabel(right_frame,text='', image=CTkImage(dark_image=source_image,size=source_image.size))
    source_image_label.grid(row=3, column=0, padx=5, pady=5)
    
    dest_image = Image.open(loaded_dest_image)
    dest_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT))
    dest_image_label = CTkLabel(right_frame,text='', image=CTkImage(dark_image=dest_image,size=dest_image.size))
    dest_image_label.grid(row=3, column=1, padx=5, pady=5)
    
    result_image = Image.open(loaded_result_image)
    result_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT))
    result_image_label = CTkLabel(right_frame,text='', image=CTkImage(dark_image=result_image,size=result_image.size))
    result_image_label.grid(row=3, column=2, padx=5, pady=5)
    
    # buttons to load files
    button_explore = CTkButton(right_frame, text = "Source image", command = lambda:browseFiles(source_image_label,'src')) 
    button_explore.grid(row=4,column = 0,padx=5, pady=5)
    
    button_explore = CTkButton(right_frame, text = "Dest image", command = lambda:browseFiles(dest_image_label,'dest')) 
    button_explore.grid(row=4,column = 1,padx=5, pady=5)
    
    button_explore = CTkButton(right_frame, text = "Result image", command = lambda:browseFiles(result_image_label,'result')) 
    button_explore.grid(row=4,column = 2,padx=5, pady=5)
    
    window.mainloop()