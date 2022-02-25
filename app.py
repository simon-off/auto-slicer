# File
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


# Root window
root = tk.Tk()
root.title('AutoSlicer')


def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif"),)
    # show the open file dialog
    audio_file = fd.askopenfile(filetypes=filetypes)


def export_file():
    pass


# Import/Export buttons
import_button = ttk.Button(root, text='Import', command=import_file)
export_button = ttk.Button(root, text='Export', command=export_file)
# Draw buttons
import_button.grid(row=2, column=0)
export_button.grid(row=2, column=1)


root.mainloop()