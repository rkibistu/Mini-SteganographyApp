from tkinter import *
from tkinter import filedialog
import steganography as steg


default_iamge_path = 'images/question.png'
loaded_image_path = default_iamge_path
secret_image_path = 'images/secret.png'
temp_image_path = default_iamge_path


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
    new_image = PhotoImage(file=loaded_image_path)
    new_image = new_image.subsample(3,3) 
    original_image_label.configure(image=new_image)
    original_image_label.image = new_image
    
def select_directory():
    global loaded_image_path
    global secret_image_path
    if(loaded_image_path == default_iamge_path):
        return
    
    folder_path = filedialog.askdirectory()
    secret_image_path = folder_path
    
def hide_message(secret_message_entry, mode):
    global loaded_image_path
    secret = secret_message_entry.get()
    print(secret)
    print(loaded_image_path)
    if(mode=="EOF"):
        temp_image_path=steg.append_after(loaded_image_path,secret)
        print(temp_image_path)
        

def open_secret_message_window(root_window):
    window = Toplevel(root_window)
    window.title("Secret message")
    window.configure(background="skyblue")

    # Create left and right frames
    left_frame = Frame(window, width=400, height=600, bg='grey')
    left_frame.grid(row=0, column=0, padx=10, pady=5)

    right_frame = Frame(window, width=850, height=600, bg='grey')
    right_frame.grid(row=0, column=1, padx=10, pady=5)

    # Create a File Explorer label
    label_file_explorer = Label(left_frame, 
                                text = "Original Image")
    label_file_explorer.grid(row=0,column = 0,padx=5, pady=5)

    # load image
    image = PhotoImage(file=loaded_image_path)
    original_image = image.subsample(3,3)  # resize image using subsample
    original_image_label = Label(left_frame, image=original_image)
    original_image_label.grid(row=1, column=0, padx=5, pady=5)
    
    # fiel explorer button
    button_explore = Button(left_frame, 
                        text = "Browse Files",
                        command = lambda:browseFiles(original_image_label)) 
    button_explore.grid(row=2,column = 0,padx=5, pady=5)
    
    
    # Create tool bar frame
    tool_bar = Frame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    
    secret_message_entry = Entry(tool_bar)
    Label(tool_bar, text="Secret:").grid(row=0, column=0, padx=5, pady=3, ipadx=10) 
    secret_message_entry.grid(row=0, column=1, padx=5, pady=3, ipadx=10, sticky='ew') 

    # Example labels that serve as placeholders for other widgets
    Label(tool_bar, text="METHODS:").grid(row=3, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=2) 

    # Example labels that could be displayed under the "Tool" menu
    Button(tool_bar, text="After EOF", command=lambda:hide_message(secret_message_entry,"EOF")).grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="Metadata").grid(row=5, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="LSB").grid(row=6, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="DCT").grid(row=7, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    
    # Display image in right_frame
    Label(right_frame, image=image).grid(row=0,column=0, padx=5, pady=5)
    Button(right_frame, text='Save', width=20, command=lambda:select_directory()).grid(row=1,column=0, padx=5, pady=5, sticky='w')

    window.mainloop()

