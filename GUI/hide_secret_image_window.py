from customtkinter import *
from customtkinter import filedialog
import steganography as steg
import shutil
import os
from PIL import Image
from GUI.settings import * 

default_iamge_path = 'images/question.png'
loaded_image_path = default_iamge_path
secret_image_path = 'images/secret.png'
temp_image_path = 'temp/temp.png'


def browseFiles(original_image_label):
    global loaded_image_path
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
    new_image.thumbnail((SMALL_IMG_WIDTH,SMALL_IMG_HEIGHT)) 
    original_image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
    original_image_label.image = CTkImage(dark_image=new_image,size=new_image.size)
    
def select_directory():
    global loaded_image_path
    global secret_image_path
    global temp_image_path
    if(loaded_image_path == default_iamge_path):
        return
    
    folder_path = filedialog.askdirectory()
    secret_image_path = folder_path
    print(temp_image_path)
    print("Save image to: ", secret_image_path + 'gen_append.png')
    
    shutil.copy(temp_image_path,secret_image_path + '/gen_append.png')
    os.remove(temp_image_path)
    
def hide_message(secret_message_entry,generated_image_label, mode):
    global loaded_image_path
    global temp_image_path
    secret = secret_message_entry.get()
    if(mode=="EOF"):
        steg.append_after(loaded_image_path,temp_image_path,secret)
    elif(mode=="metadata"):
        steg.hide_inside_metadata(loaded_image_path,temp_image_path, secret)
    elif(mode=="lsb"):
        steg.hide_message_inside_lsb(loaded_image_path,temp_image_path,secret,"!")
    elif(mode=="dct"):
        steg.hide_message_inside_dct(loaded_image_path,temp_image_path,secret)
    elif():
        print("Wrong mode: ",mode)
        return
    print("Temp saved to: ",temp_image_path, " with secret: ",secret)
        
    
    # Change label contents
    loaded_image_path = temp_image_path 
    new_image = Image.open(loaded_image_path)
    new_image.thumbnail((BIG_IMG_WIDTH,BIG_IMG_HEIGHT))
    generated_image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
    generated_image_label.image = CTkImage(dark_image=new_image,size=new_image.size)

def open_hide_secret_message_window(root_window):
    #reset to default settings everytime it opens
    global loaded_image_path
    global secret_image_path
    global temp_image_path
    loaded_image_path = default_iamge_path
    secret_image_path = 'images/secret.png'
    temp_image_path = 'temp/temp.png'
    
    window = CTkToplevel(root_window)
    window.title("Secret message")
    window.configure(background="skyblue")
    window.grab_set()

    # Create left and right frames
    left_frame = CTkFrame(window, width=400, height=600)
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = CTkFrame(window, width=850, height=600)
    right_frame.grid(row=0, column=1, padx=10, pady=5)
    
   

    # Create a File Explorer labels
    label_file_explorer = CTkLabel(left_frame, 
                                text = "Original Image")
    label_file_explorer.grid(row=0,column = 0,padx=5, pady=5)

    # load image
    image = Image.open(loaded_image_path)
    original_image = image.copy()  # resize image using subsample
    original_image.thumbnail((SMALL_IMG_WIDTH,SMALL_IMG_HEIGHT))
    original_image_label = CTkLabel(left_frame,text='', image=CTkImage(dark_image=original_image,size=original_image.size))
    original_image_label.grid(row=1, column=0, padx=5, pady=5)
    
    #shoed in tight panel, contains the secret
    image.thumbnail((BIG_IMG_WIDTH,BIG_IMG_HEIGHT))
    generated_image = CTkLabel(right_frame,text='', image=CTkImage(dark_image=image,size=image.size))
    
    # fiel explorer button
    button_explore = CTkButton(left_frame, 
                        text = "Browse Files",
                        command = lambda:browseFiles(original_image_label)) 
    button_explore.grid(row=2,column = 0,padx=5, pady=5)
    
    
    # Create tool bar frame
    tool_bar = CTkFrame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    
    secret_message_entry = CTkEntry(tool_bar)
    CTkLabel(tool_bar, text="Secret:").grid(row=0, column=0, padx=5, pady=3, ipadx=10) 
    secret_message_entry.grid(row=0, column=1, padx=5, pady=3, ipadx=10, sticky='ew') 

    # Example labels that serve as placeholders for other widgets
    CTkLabel(tool_bar, text="METHODS:").grid(row=3, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=2) 

    # Example labels that could be displayed under the "Tool" menu
    CTkButton(tool_bar, text="After EOF", command=lambda:hide_message(secret_message_entry,generated_image,"EOF")).grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="Metadata", command=lambda:hide_message(secret_message_entry,generated_image,"metadata")).grid(row=5, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="LSB", command=lambda:hide_message(secret_message_entry,generated_image,"lsb")).grid(row=6, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="DCT", command=lambda:hide_message(secret_message_entry,generated_image,"dct")).grid(row=7, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    
    # Display image in right_frame
    generated_image.grid(row=0,column=0, padx=5, pady=5)
    CTkButton(right_frame, text='Save', width=20, command=lambda:select_directory()).grid(row=1,column=0, padx=5, pady=5, sticky='w')

    window.mainloop()

