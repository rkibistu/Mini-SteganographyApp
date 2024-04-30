from tkinter import *
from tkinter import filedialog
import steganography as steg


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
    new_image = PhotoImage(file=loaded_image_path)
    new_image_mini = new_image.subsample(3,3) 
    original_image_label.configure(image=new_image_mini)
    original_image_label.image = new_image_mini
    
    right_image_label.configure(image=new_image)
    right_image_label.image = new_image
    
    
def extract_message(secret_message_label, mode):
    global loaded_image_path

    result = ''
    if(mode=="EOF"):
        result = steg.extract_append_after(loaded_image_path)
        
    secret_message_label.configure(text=result)
    print(result)

def open_extract_secret_message_window(root_window):
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
    
    right_panel_image = Label(right_frame, image=image)
    
    # fiel explorer button
    button_explore = Button(left_frame, 
                        text = "Browse Files",
                        command = lambda:browseFiles(original_image_label,right_panel_image)) 
    button_explore.grid(row=2,column = 0,padx=5, pady=5)
    
    
    # Create tool bar frame
    tool_bar = Frame(left_frame, width=180, height=185)
    tool_bar.grid(row=3, column=0, padx=5, pady=5, sticky='ew')
    
    secret_message_label = Label(right_frame)

    #this 3 liens are used just for alignement, they are not shown in the app
    secret_message_entry = Entry(tool_bar)
    Label(tool_bar, text="Secret:").grid(row=0, column=0, padx=5, pady=3, ipadx=10,sticky='ew') 
    secret_message_entry.grid(row=0, column=1, padx=5, pady=3, ipadx=10, sticky='ew') 
    
    # Example labels that serve as placeholders for other widgets
    Label(tool_bar, text="METHODS:").grid(row=0, column=0, padx=5, pady=3, ipadx=10, sticky='ew', columnspan=10) 

    # Example labels that could be displayed under the "Tool" menu
    Button(tool_bar, text="After EOF", command=lambda:extract_message(secret_message_label,"EOF")).grid(row=1, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="Metadata").grid(row=2, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="LSB").grid(row=3, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    Button(tool_bar, text="DCT").grid(row=4, column=0, padx=5, pady=5, sticky='ew', columnspan=2)
    
    
    # Display image in right_frame
    right_panel_image.grid(row=0,column=0, padx=5, pady=5)
    Label(right_frame,text="Secret: ").grid(row=1, column=0, padx=5, pady=3, ipadx=10, sticky='w') 
    secret_message_label.grid(row=1, column=1, padx=5, pady=3, ipadx=10, sticky="ew", columnspan=10) 
    window.mainloop()

