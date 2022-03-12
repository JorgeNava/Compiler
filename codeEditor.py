from tkinter import *
import tkinter.filedialog as fd
import tkinter.messagebox as mb

from PIL import Image, ImageTk
import os

# Creating all the functions of all the buttons in the NotePad
def open_file():
    global file
    file = fd.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ("Text File", "*.txt*")])
    if file != '':
        root.title(f"{os.path.basename(file)}")
        text_area.delete(1.0, END)
        with open(file, "r") as file_:
            text_area.insert(1.0, file_.read())
            file_.close()
    else:
        file = None


def open_new_file():
    root.title("Untitled - JGCodeEditor")
    text_area.delete(1.0, END)


def save_file():
    global file
    if file == '':
        file = None
    else:
        file = open(file, "w")
        file.write(text_area.get(1.0, END))
        file.close()

    if file is None:
        file = fd.asksaveasfilename(initialfile='Untitled.txt', defaultextension='.txt',
                                    filetypes=[("Text File", "*.txt*"), ("Word Document", '*,docx*'), ("PDF", "*.pdf*")])
    else:
        file = open(file, "w")
        file.write(text_area.get(1.0, END))
        file.close()
        root.title(f"{os.path.basename(file)} - Notepad")


def exit_application():
    root.destroy()


def copy_text():
    text_area.event_generate("<<Copy>>")


def cut_text():
    text_area.event_generate("<<Cut>>")


def paste_text():
    text_area.event_generate("<<Paste>>")


def select_all():
    text_area.event_generate("<<Control-Keypress-A>>")


def delete_last_char():
    text_area.event_generate("<<KP_Delete>>")

def runCode():
    if file.endswith(".jg"):
        os.system("python main.py")

# Initializing the window
root = Tk()
root.title("Untitled - JGCodeEditor")
root.geometry('800x500')
root.resizable(0, 0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

icon = ImageTk.PhotoImage(Image.open('Notepad.png'))
root.iconphoto(False, icon)
file = ''

# Setting the basic components of the window
menu_bar = Menu(root)
root.config(menu=menu_bar)

text_area = Text(root, font=("Consolas", 12))
text_area.grid(sticky=NSEW)
text_area.config(bg ="BLACK", fg="LIGHTGREEN")

scroller = Scrollbar(text_area, orient=VERTICAL)
scroller.pack(side=RIGHT, fill=Y)

scroller.config(command=text_area.yview)
text_area.config(yscrollcommand=scroller.set)

# Adding the File Menu and its components
file_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
file_menu.add_command(label="New", command=open_new_file)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save As", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Close File", command=exit_application)

menu_bar.add_cascade(label="File", menu=file_menu)

# Adding the Edit Menu and its components
edit_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
edit_menu.add_command(label='Copy', command=copy_text)
edit_menu.add_command(label='Cut', command=cut_text)
edit_menu.add_command(label='Paste', command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', command=select_all)
edit_menu.add_command(label='Delete', command=delete_last_char)

menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Adding the Code Menu and its components
code_menu = Menu(menu_bar, tearoff=False, activebackground='DodgerBlue')
code_menu.add_command(label='Run code', command=runCode)

menu_bar.add_cascade(label="Code", menu=code_menu)

root.config(menu=menu_bar)

# Finalizing the window
root.update()
root.mainloop()
