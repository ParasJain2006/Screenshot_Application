import time
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab
from tkinter import filedialog
from tkinter import font

root = tk.Tk()
root.title("Application Window")
root.geometry("+300+100")

#menu bar functions
path=None
def view_previous():
    if(path):
        os.startfile(path)

def open_folder():
    folder_path= filedialog.askdirectory()
    if(folder_path):
        os.startfile(folder_path)

# Create a Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Create an "view" menu
view = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="View", menu=view)
view.add_command(label="View Folder",font=font.Font(family="Times New Roman", size=11 ),command=open_folder)
view.add_command(label="View Last screenshot",font=font.Font(family="Times New Roman", size=11),command=view_previous)

# Create an "Exit" menu
def exit_application():
    root.quit()
menu_bar.add_command(label="Exit", command=exit_application)


# Create a Notebook widget
notebook = ttk.Notebook(root)

#styling
style=ttk.Style()
style.configure("TFrame", background="lightblue", foreground="black")
style.configure("TNotebook.Tab", padding=(54, 7))
style.configure("TNotebook.Tab", font=("Times New Roman", 11,"bold"))
style.configure("TButton",font=("Times New Roman", 13), padding=(10, 5),relief=tk.RAISED)

# Create tabs
tab_about = ttk.Frame(notebook,style="TFrame")
tab_single_screenshot = ttk.Frame(notebook,style="TFrame")
tab_multiple_screenshot = ttk.Frame(notebook,style="TFrame")

# Add tabs to the Notebook
notebook.add(tab_about, text="About")
notebook.add(tab_single_screenshot, text="Single Screenshot")
notebook.add(tab_multiple_screenshot, text="Multiple Screenshots")

# Place the Notebook widget
notebook.pack(fill=tk.BOTH, expand=True)

#single capture functions
def capture_single():
    status_label=tk.Label(tab_single_screenshot, text="")
    status_label.grid(row=3,column=0,columnspan=3,pady=20)
    
    root.withdraw()
    time.sleep(0.2)

    screenshot = ImageGrab.grab()
    global path
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    path=save_path
    if save_path:
        screenshot.save(save_path)
        status_label.config(text=f"Screenshot saved as {os.path.basename(save_path)}",font=("Times New Roman",13))

    root.deiconify()
    folder_message = ttk.Label(root, text=f"Screenshots saved in folder: {save_path}  :)")
    folder_message.pack(pady=20)

def start_countdown(delay):
    countdown_label=ttk.Label(tab_single_screenshot, text="")
    countdown_label.grid(row=3,column=0,columnspan=3)
    countdown_label.config(text=f"Taking a screenshot in {delay} seconds...",font=("Times New Roman",13))
    tab_single_screenshot.update()  # Update the GUI to show the countdown label

    for remaining_time in range(delay, -1, -1):
        countdown_label.config(text=f"Taking a screenshot in {remaining_time} seconds...")
        tab_single_screenshot.update()  # Update the GUI to show the updated countdown label
        time.sleep(1)

    countdown_label.grid_forget()

def capture_delay():
    e=(delay_entry.get())
    if(e.isdigit()):
        delay=int(e)
    else:
        error_label=ttk.Label(tab_single_screenshot,text="Incorrect Input :(")
        error_label.config(font=("Times New Roman",12))
        error_label.grid(row=3,column=0,columnspan=3,pady=10)
    start_countdown(delay)
    root.withdraw()
    time.sleep(0.1)
    capture_single()
    root.deiconify()

def capture_multiple():
    try:
        e=entry.get()
        if e.isdigit():
            n=int(e)
             # Ask the user for the directory to save screenshots
            folder_path = filedialog.askdirectory(title="Select Directory to Save Screenshots")
        else:
            error_label=ttk.Label(tab_multiple_screenshot,text="Incorrect Input :(")
            error_label.config(font=("Times New Roman",12))
            error_label.grid(row=4,column=0,pady=10)
            
        if folder_path:
            # Generate a timestamp-based subdirectory name 
            timestamp = time.strftime("%Y%m%d%H%M%S")
            screenshot_dir = os.path.join(folder_path, f"screenshots_{timestamp}")
            os.makedirs(screenshot_dir, exist_ok=True)

            for i in range(n):

                root.withdraw()
                time.sleep(0.2)
                # Capture the screen
                screenshot = ImageGrab.grab()

                # Generate a unique filename for each screenshot
                screenshot_filename = f"screenshot_{i+1}.png"
                save_path = os.path.join(screenshot_dir, screenshot_filename)
                global path
                path=save_path

                # Save the screenshot
                screenshot.save(save_path)

                root.deiconify()

                # Create a new message label for each screenshot
                message_label = ttk.Label(tab_multiple_screenshot, text=f"Screenshot {i+1} saved as {screenshot_filename}")
                message_label.grid(row=3,column=0)
                message_label.config(font=("Times new Roman",12))  # Pack the message label into the window
                tab_multiple_screenshot.update()
                time.sleep(0.4)

        root.deiconify()

        folder_message = ttk.Label(root, text=f"Screenshots saved in folder: {screenshot_dir}  :)")
        folder_message.pack(pady=20,side="bottom")

    except Exception as e:
        message_label = ttk.Label(root, text="")
        message_label.pack(pady=10)
        message_label.config(text=f"Error capturing screenshot: {str(e)}")
    
#single screenshot tab layout
style = ttk.Style()
style.configure("CustomLabel.TLabel", font=("Times New Roman", 15, "bold"), foreground="black")
style.configure("Custom.TFrame",background="white")
label1=ttk.Label(tab_single_screenshot,text="SCREENSHOT APPLICATION",style="CustomLabel.TLabel")
label1.grid(row=0,column=0,columnspan=3,pady=20)

label2=ttk.Label(tab_single_screenshot,text="Single screenshots :) ")
label2.config(font=("Times New Roman",13,"bold"))
label2.grid(row=1,column=0,columnspan=3,pady=10)

frame1=ttk.Frame(tab_single_screenshot,height=10,style="Custom.TFrame")
frame1.grid(row=2,column=0,columnspan=3,pady=20)

label3=ttk.Label(frame1,text="Click capture button to take a single screenshot.")
label3.config(font=("Times New Roman", 13))
label3.grid(row=2,column=0,columnspan=2,pady=20)

capture=ttk.Button(frame1,text="Capture",command=capture_single)
capture.grid(row=2,column=2,pady=20)

delay_label=tk.Label(frame1,text=" Enter a time delay :")
delay_label.grid(row=3,column=0,columnspan=1,pady=20)
delay_label.config(font=("Times New Roman", 13))

delay_entry=ttk.Entry(frame1)
delay_entry.grid(row=3,column=1,columnspan=1,pady=20)

capture_delay=ttk.Button(frame1,text="Capture with delay",command=capture_delay)
capture_delay.grid(row=3,column=2,pady=20)

tab_single_screenshot.columnconfigure(0, weight=1)
tab_single_screenshot.columnconfigure(1, weight=1)
tab_single_screenshot.columnconfigure(2, weight=1)

#multiple screenshot tab layout

label1=ttk.Label(tab_multiple_screenshot,text="SCREENSHOT APPLICATION",style="CustomLabel.TLabel")
label1.grid(row=0,column=0,pady=20)
label2=ttk.Label(tab_multiple_screenshot,text="Multiple screenshots :) ")
label2.config(font=("Times New Roman",13,"bold"))
label2.grid(row=1,column=0,pady=0)

frame1=ttk.Frame(tab_multiple_screenshot,height=10,style="Custom.TFrame")
frame1.grid(row=2,column=0,pady=20)

label3=ttk.Label(frame1,text="Enter the no of screenshots you want :")
label3.grid(row=0,column=0,pady=20)
label3.config(font=("Times New Roman",13))

entry=ttk.Entry(frame1)
entry.grid(row=1,column=0)

capture=ttk.Button(frame1,text="Capture",command=capture_multiple)
capture.grid(row=2,column=0,pady=10)

tab_multiple_screenshot.columnconfigure(0, weight=1)

#About tab Layout

label1=ttk.Label(tab_about,text="SCREENSHOT APPLICATION",style="CustomLabel.TLabel")
label1.grid(row=0,column=0,pady=20)

label2=ttk.Label(tab_about,text="WELCOME USER :) ")
label2.config(font=("Times New Roman",12,"bold"))
label2.grid(row=1,column=0,pady=10)

description_text = """
    Screenshot Application is a simple tool designed to make capturing screenshots effortless..

    Features:

    - Capture single or multiple(burst) screenshots
    - Save screenshots at your preferred Location
    - Easy-to-use and responsive interface
    """
description_widget = tk.Text(tab_about, wrap=tk.WORD,height=10)
description_widget.insert(tk.END, description_text)
description_widget.config(state="disabled",font=("Times New Roman",12))
description_widget.grid(row=2,column=0,pady=10)

thanks=ttk.Label(tab_about,text="THANK YOU !!",font=("Times New Roman",12,"bold"))
thanks.grid(row=3,column=0,pady=(20,0))
tab_about.columnconfigure(0, weight=1)

root.mainloop()
