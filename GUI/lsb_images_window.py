from customtkinter import *
from tkinter import *
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
save_path = 'images/lsb_secret.png'
save_path1 = 'images/lsb_extracted1.png'
save_path2 = 'images/lsb_extracted2.png'

# used to keep the value from radio buttons
radio_var = 0
# used to change the label of bits sued isnide the slider event
bits_used_label = 0
# bits used
bits_used = 4

def slider_event(value):
    global bits_used_label
    global bits_used
    bits_used = int(value)
    bits_used_label.configure(text=('Bits for secret: ' + str(int(value))))
    
def radiobutton_event():
    global radio_var
    print("radiobutton toggled, current value:", radio_var.get())
    
def browseFiles(image_label, mode):
    global loaded_source_image
    global loaded_dest_image
    global loaded_result_image
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files",
                                                        "*.*")
                                                        ,("PNG files",
                                                        "*.png")))
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
        
def show_bitplanes():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files",
                                                        "*.*")
                                                        ,("PNG files",
                                                        "*.png")))
    if(filename == ''):
        return 
    
    bitplane_img = steg.bitplanes2(filename,"images/bitplane.png")
    bitplane_img.show()
        
def hide_image(source_iamge_label, dest_image_label, result_image_label):
    global loaded_source_image
    global loaded_dest_image
    global loaded_result_image
    result = 1
    if(radio_var.get() == 1):
        #hide
        print("hide")
        res = steg.hide_image_inside_lsb(loaded_source_image,loaded_dest_image, save_path,bits_used)
        loaded_result_image = save_path
        
        if(res == -1):
            print("failed")
            return
        print("ok")
        # Change label contents
        loaded_image_path = save_path 
        new_image = Image.open(loaded_image_path)
        new_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT)) 
        result_image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
        result_image_label.image = CTkImage(dark_image=new_image,size=new_image.size)
    if(radio_var.get() == 2):
        #extract
        print("extract")
        res = steg.extract_image_from_lsb(loaded_result_image,save_path1,save_path2,bits_used)
        loaded_source_image = save_path1
        loaded_dest_image = save_path2
        
        # Change label contents
        loaded_image_path = save_path1 
        new_image = Image.open(loaded_image_path)
        new_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT)) 
        source_iamge_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
        source_iamge_label.image = CTkImage(dark_image=new_image,size=new_image.size)
        
        loaded_image_path = save_path2
        new_image = Image.open(loaded_image_path)
        new_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT)) 
        dest_image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
        dest_image_label.image = CTkImage(dark_image=new_image,size=new_image.size)

def open_lsb_images_window(root_window):
    #reset to default settings everytime it opens
    global loaded_source_image
    global loaded_dest_image
    global loaded_result_image
    global radio_var
    global bits_used_label
    loaded_source_image = default_loaded_image
    loaded_dest_image = default_loaded_image
    loaded_result_image = default_loaded_image
    radio_var = IntVar(root_window,0)

    window = CTkToplevel(root_window)
    window.title("Image inside image")
    window.configure(background="skyblue")
    window.grab_set()
    
    source_image = Image.open(loaded_source_image)
    dest_image = Image.open(loaded_dest_image)
    result_image = Image.open(loaded_result_image)

    # Create left and right frames
    left_frame = CTkFrame(window, width=400, height=600)
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = CTkFrame(window, width=850, height=600)
    right_frame.grid(row=0, column=1, padx=10, pady=5)
    
    #left frame
    CTkLabel(left_frame, text = "DIRECTION:").grid(row=0,column = 0,padx=5, pady=5)
    #add radio button here
    radiobutton_1 = CTkRadioButton(left_frame, text="Hide",
                                             command=radiobutton_event, variable= radio_var, value=1)
    radiobutton_2 = CTkRadioButton(left_frame, text="Extract",
                                             command=radiobutton_event, variable= radio_var, value=2)
    radiobutton_1.grid(row=1,column = 0,padx=5, pady=5, sticky='ew', columnspan=4)
    radiobutton_2.grid(row=2,column = 0,padx=5, pady=5, sticky='ew', columnspan=4)
    
    # Create tool bar frame with accepted methods
    tool_bar = CTkFrame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

    # Example labels that serve as placeholders for other widgets
    CTkLabel(tool_bar, text="METHODS:").grid(row=3, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=2) 

    # Example labels that could be displayed under the "Tool" menu
    CTkButton(tool_bar, text="Basic LSB", command=lambda:hide_image(source_image_label, dest_image_label, result_image_label)).grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="XOR").grid(row=5, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    CTkLabel(left_frame, text="EXTRA:").grid(row=4, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=2) 
    CTkButton(left_frame,text="Show all planes", command=show_bitplanes).grid(row=5, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
       
    # Display objects in right_frame
    CTkLabel(right_frame,text='Lets\' hide some images').grid(row=0,column=0, padx=5, pady=5, sticky='new', columnspan=10)
    bits_used_label = CTkLabel(right_frame,text='Bits for secret: 4')
    bits_used_label.grid(row=1,column=0, padx=5, pady=5, sticky='new', columnspan=10)
    bitsSlider = CTkSlider(master=right_frame, from_=1, to=8, command=slider_event, number_of_steps=7)
    bitsSlider.grid(row=2,column=0, padx=5, pady=5, sticky='ew', columnspan=10)
    
    # 3 images
    source_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT))
    source_image_label = CTkLabel(right_frame,text='', image=CTkImage(dark_image=source_image,size=source_image.size))
    source_image_label.grid(row=3, column=0, padx=5, pady=5)
    
    dest_image.thumbnail((LSB_IMG_WIDTH,LSB_IMG_HEIGHT))
    dest_image_label = CTkLabel(right_frame,text='', image=CTkImage(dark_image=dest_image,size=dest_image.size))
    dest_image_label.grid(row=3, column=1, padx=5, pady=5)
    
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