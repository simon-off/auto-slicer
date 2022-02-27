# Tkinter
import tkinter as tk
from tkinter import OFF, ttk
from tkinter import filedialog as fd
# PyDub
from pydub import AudioSegment
# MatPlotLib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
plt.style.use("./waveform.mplstyle")
# Numpy
import numpy


# Root window
root = tk.Tk()
root.title('AutoSlicer')
root.geometry("1200x300")
root.configure(bg="#333")


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
    mono = mono.set_sample_width(2)
    samples = mono.get_array_of_samples()
    # Get the seconds for plotting X
    fps = mono.frame_rate
    time = numpy.linspace(0, len(samples)/fps, num=len(samples))
    # Plot the waveform with the samples
    fig = plt.figure()
    waveplot = fig.add_subplot(111)
    waveplot.plot(time, samples, color="#FF8800")
    waveplot.set_yticks([-32768, -16384, 0, 16384, 32767])
    # Draw the plot with Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, columnspan=2, sticky="NSEW")


def export_file():
    pass



# Frame for button row
frame = tk.Frame(root)
frame.grid(row=1, columnspan=3, sticky="SEW")
frame.configure(background="#444")

# Import/Export buttons
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