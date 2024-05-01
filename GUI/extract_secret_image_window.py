from customtkinter import *
from customtkinter import filedialog
import steganography as steg
from PIL import Image
from GUI.settings import *

default_iamge_path = 'images/question.png'
loaded_image_path = default_iamge_path
secret_image_path = 'images/secret.png'
temp_image_path = default_iamge_path


def browseFiles(original_image_label, right_image_label):
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
    new_image_mini = new_image.copy()
    new_image_mini.thumbnail((SMALL_IMG_WIDTH,SMALL_IMG_HEIGHT))
    original_image_label.configure(image=CTkImage(dark_image=new_image_mini,size=new_image_mini.size))
    original_image_label.image = new_image_mini
    
    new_image.thumbnail((BIG_IMG_WIDTH,BIG_IMG_HEIGHT))
    right_image_label.configure(image=CTkImage(dark_image=new_image,size=new_image.size))
    right_image_label.image = new_image
    
    
def extract_message(secret_message_label, mode):
    global loaded_image_path

    result = ''
    if(mode=="EOF"):
        result = steg.extract_append_after(loaded_image_path)
    elif(mode=="metadata"):
        result = steg.extract_from_metada(loaded_image_path)
    elif(mode=="lsb"):
        result = steg.exctract_messge_from_lsb(loaded_image_path,"!")
    else:
        print("Wrong mode: ",mode)
        return
                
    secret_message_label.configure(text=result)
    print(result)

def open_extract_secret_message_window(root_window):
    window = CTkToplevel(root_window)
    window.title("Secret message")
    window.configure(background="skyblue")
    window.grab_set()


    # Create left and right frames
    left_frame = CTkFrame(window, width=400, height=600)
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = CTkFrame(window, width=850, height=600)
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # Create a File Explorer label
    label_file_explorer = CTkLabel(left_frame, 
                                text = "Original Image")
    label_file_explorer.grid(row=0,column = 0,padx=5, pady=5)

    # load image
    image = Image.open(loaded_image_path)
    original_image = image.copy()
    original_image.thumbnail((SMALL_IMG_WIDTH,SMALL_IMG_HEIGHT))
    original_image_label = CTkLabel(left_frame,text='', image=CTkImage(dark_image=original_image,size=original_image.size))
    original_image_label.grid(row=1, column=0, padx=5, pady=5)
    
    image.thumbnail((BIG_IMG_WIDTH,BIG_IMG_HEIGHT))
    right_panel_image = CTkLabel(right_frame,text='', image=CTkImage(dark_image=image,size=image.size))
    
    # fiel explorer button
    button_explore = CTkButton(left_frame, 
                        text = "Browse Files",
                        command = lambda:browseFiles(original_image_label,right_panel_image)) 
    button_explore.grid(row=2,column = 0,padx=5, pady=5)
    
    
    # Create tool bar frame
    tool_bar = CTkFrame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    
    secret_message_label = CTkLabel(right_frame)

    #this 3 liens are used just for alignement, they are not shown in the app
    secret_message_entry = CTkEntry(tool_bar)
    CTkLabel(tool_bar, text="Secret:").grid(row=0, column=0, padx=5, pady=3, ipadx=10,sticky='ew') 
    secret_message_entry.grid(row=0, column=1, padx=5, pady=3, ipadx=10, sticky='ew') 
    
    # Example labels that serve as placeholders for other widgets
    CTkLabel(tool_bar, text="METHODS:").grid(row=0, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=10) 

    # Example labels that could be displayed under the "Tool" menu
    CTkButton(tool_bar, text="After EOF", command=lambda:extract_message(secret_message_label,"EOF")).grid(row=1, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="Metadata", command=lambda:extract_message(secret_message_label,"metadata")).grid(row=2, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="LSB", command=lambda:extract_message(secret_message_label,"lsb")).grid(row=3, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    CTkButton(tool_bar, text="DCT", command=lambda:extract_message(secret_message_label,"dct")).grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    
    # Display image in right_frame
    right_panel_image.grid(row=0,column=0, padx=5, pady=5)
    CTkLabel(right_frame,text="Secret: ").grid(row=1, column=0, padx=5, pady=3, ipadx=10, sticky='w') 
    secret_message_label.grid(row=1, column=1, padx=5, pady=3, ipadx=10, sticky="ew", columnspan=10) 
    window.mainloop()

