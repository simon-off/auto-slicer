# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
# PyDub
from pydub import AudioSegment
# MatPlotLib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Numpy
import numpy


# MatPlotLib Stylesheet
plt.style.use("./waveform.mplstyle")


# Root window
root = tk.Tk()
root.title('AutoSlicer')
root.geometry("1250x250")
root.resizable(False, False)
root.configure(bg="#333")


# Import and load imput_sample to PyDub
def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif *.ogg"),)
    filepath = fd.askopenfile(filetypes=filetypes).name
    audio_file = AudioSegment.from_file(filepath)
    plot_waveform(audio_file)


# Plot waveform via matplotlib
def plot_waveform(audio_file):
    # Convert audio to 16Bit mono and get array of sample data
    samples = audio_file.set_channels(1).set_sample_width(2).get_array_of_samples()
    # Plot the waveform with the samples
    fig = plt.figure(dpi=50)
    waveplot = fig.add_subplot(111)
    waveplot.plot(samples, color="#FF8800")
    waveplot.set_yticks([-32768, -16384, 0, 16384, 32767])
    # Draw the plot with Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, sticky="NSEW")


# Export Sliced Sample(s)
def export_file():
    pass


# Frame for button row
frame = tk.Frame(root)
frame.grid(row=1, sticky="SEW")
frame.configure(background="#444")

# Buttons
import_button = tk.Button(frame, text="Import", command=import_file)
threshold_input = tk.Spinbox(frame)
fade_in_input = tk.Spinbox(frame)
fade_out_input = tk.Spinbox(frame)
normalize_button = tk.Checkbutton(frame, text="Normalize")
normalize_button.deselect()
export_button = tk.Button(frame, text="Export", command=export_file)

# Draw buttons
buttons = [
    import_button,
    threshold_input,
    fade_in_input,
    fade_out_input,
    normalize_button,
    export_button
]

for i, button in enumerate(buttons):
    button.grid(row=1, column=i, sticky="NSEW")

# Configure grid
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(frame, list(range(len(buttons))), weight=1)


root.mainloop()