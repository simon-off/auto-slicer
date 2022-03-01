# Tkinter
import tkinter as tk
from tkinter import ttk, font
from tkinter import filedialog as fd
from turtle import right
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
root.configure(bg="#111")
# Font
#defaultFont = font.nametofont("TkDefaultFont")
#defaultFont.configure(family="Roboto Mono", size=10)


# Import and load imput_sample to PyDub
def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif *.ogg"),)
    filepath = fd.askopenfile(filetypes=filetypes).name
    global audio_file
    audio_file = AudioSegment.from_file(filepath)
    plot_waveform()


# Plot waveform via matplotlib
def plot_waveform():
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
time_frame = tk.Frame(root, bg="#666")
time_frame.grid(row=1, sticky="SEW")
test_label = tk.Label(time_frame, text="TESTING")
test_label.grid()
# Frame for button row
frame = tk.Frame(root, bg="#444")
frame.grid(row=2, sticky="SEW")

# Frame Widgets
import_button = tk.Button(frame, text="Import", command=import_file)
threshold_label = tk.Label(frame, text="Threshold ", anchor="e")
threshold_input = tk.Scale(frame, from_=0, to=-100, orient="horizontal", showvalue=False, highlightthickness=0)
fade_in_label = tk.Label(frame, text="Fade in ", anchor="e")
fade_in_input = tk.Spinbox(frame, from_=0, to=1000)
fade_out_label = tk.Label(frame, text="Fade out ", anchor="e")
fade_out_input = tk.Spinbox(frame, from_=0, to=1000)
normalize_button = tk.Checkbutton(frame, text="Normalize")
normalize_button.deselect()
export_button = tk.Button(frame, text="Export", command=export_file)

# Draw Frame Widgets
buttons = [
    import_button,
    threshold_label,
    threshold_input,
    fade_in_label,
    fade_in_input,
    fade_out_label,
    fade_out_input,
    normalize_button,
    export_button
]

for i, button in enumerate(buttons):
    button.grid(row=1, column=i, sticky="NSEW")
    button.configure(bg="#222", fg="#FFF", activebackground="#333")

# Configure grid
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(frame, list(range(len(buttons))), weight=1)


root.mainloop()