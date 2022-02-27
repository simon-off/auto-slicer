# Tkinter
from importlib import resources
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.pyplot import tight_layout
# PyDub
from pydub import AudioSegment
# MatPlotLib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
plt.style.use("./waveform.mplstyle")


# Root window
root = tk.Tk()
root.title('AutoSlicer')
root.geometry("1080x270")


# Import and load imput_sample to PyDub
def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif"),)
    filepath = fd.askopenfile(filetypes=filetypes).name
    audio_file = AudioSegment.from_file(filepath)
    plot_waveform(audio_file)


# Plot waveform via matplotlib
def plot_waveform(audio_file):
    # Convert audio to mono and get array och sample data
    mono = audio_file.set_channels(1)
    samples = mono.get_array_of_samples()
    # Plot the waveform with the samples
    fig = plt.figure()
    waveplot = fig.add_subplot(111)
    waveplot.plot(samples)
    # Draw the plot with Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, columnspan=2, sticky="NSEW")


def export_file():
    pass


# Configure grid
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

# Import/Export buttons
import_button = ttk.Button(root, text='Import', command=import_file)
export_button = ttk.Button(root, text='Export', command=export_file)
# Draw buttons
import_button.grid(row=1, column=0, sticky="SEW")
export_button.grid(row=1, column=1, sticky="SEW")


root.mainloop()