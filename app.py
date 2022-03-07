# Tkinter
import tkinter as tk
from tkinter import HORIZONTAL, ttk, font
from tkinter import filedialog as fd
from turtle import right
# PyDub
from pydub import AudioSegment, silence
# MatPlotLib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# Numpy
import numpy
# Math
import math


# MatPlotLib Stylesheet
plt.style.use("./waveform.mplstyle")


# Define global variables
filepath = None
audio_file = None
line_canvas = None
threshold = 0


# Root window
root = tk.Tk()
root.title('AutoSlicer')
root.geometry("1250x250")
root.configure(bg="#191919")
# Font
#defaultFont = font.nametofont("TkDefaultFont")
#defaultFont.configure(family="Roboto Mono", size=10)


# Frame to draw graph and lines
main_frame = tk.Frame(root, bg="#191919")
main_frame.grid(row=0, sticky="NSEW")


# Import and load imput_sample to PyDub
def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif *.ogg"),)
    global filepath
    filepath = fd.askopenfile(filetypes=filetypes).name
    global audio_file
    audio_file = AudioSegment.from_file(filepath)
    plot_waveform()
    filepath_label.config(text = filepath)
    audio_length_label.config(text = str(round(audio_file.duration_seconds, 3)) + " SECONDS")


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
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, sticky="NSEW")
    canvas.get_tk_widget().configure(background='black')

    # Add threshold line
    global line_canvas
    line_canvas = tk.Canvas(main_frame)
    draw_lines()


# Update and draw Threshold Line
def draw_lines():
    if line_canvas != None:
        line_canvas.configure(bg="#0099FF", height=2, highlightthickness=0)
        line_canvas.place(relwidth=100, rely=((-threshold / 200) - 0.002 + 0.5))


# Command that runs when changing the threshold value
def update_threshold(trash):
    input = threshold_input.get()
    threshold_value.config(text=input)
    if input and int(input) >= 0 and int(input) <= 100:
        global threshold
        threshold = int(input)
        draw_lines()
        return True
    else:
        return False

thresh=root.register(update_threshold)


# Export Sliced Sample(s)
def export_file():
    if filepath != None:
        # calculate proper dbfs values for the split_on_silence function
        threshold_16 = numpy.interp(threshold, [0, 100], [0, 32768])
        valueDBFS = round(20 * math.log10(abs(threshold_16)/32768), 1)
        export_folder = fd.askdirectory()
        slices = silence.split_on_silence(audio_file, silence_thresh=valueDBFS)
        for i, slice in enumerate(slices):
            with open("{}/sound-{}.wav".format(export_folder, i), "wb") as f:
                slice.export(f, format="wav")


# Draw button_frame for label row
info_frame = tk.Frame(root, bg="#111")
info_frame.grid(row=1, sticky="EW")
# Filepath
filepath_label = tk.Label(info_frame, bg="#111", fg="#666", padx=5)
filepath_label.grid(sticky="W", row=0, column=0)
# Audio length
audio_length_label = tk.Label(info_frame, bg="#111", fg="#666", padx=5)
audio_length_label.grid(sticky="E", row=0, column=0)


# Frame for button row
button_frame = tk.Frame(root, bg="#222", bd=1)
button_frame.grid(row=2, sticky="SEW")


# Button Widgets
import_button = tk.Button(button_frame, text="Import", command=import_file)

threshold_label = tk.Label(button_frame, text="Threshold ", anchor="e")
#threshold_input = tk.Spinbox(button_frame, from_=0, to=100)
threshold_input = tk.Scale(button_frame, showvalue=False, orient=HORIZONTAL, from_=0, to=100, command=update_threshold)
threshold_value = tk.Label(button_frame, text=0, anchor="w")
#threshold_input.config(validate="all", validatecommand=(thresh, '%P'))

fade_in_label = tk.Label(button_frame, text="Fade in ", anchor="e")
fade_in_input = tk.Spinbox(button_frame, from_=0, to=1000)

fade_out_label = tk.Label(button_frame, text="Fade out ", anchor="e")
fade_out_input = tk.Spinbox(button_frame, from_=0, to=1000)

normalize_button = tk.Checkbutton(button_frame, text="Normalize")
normalize_button.deselect()

export_button = tk.Button(button_frame, text="Export", command=export_file)


# Draw Frame Widgets
buttons = [
    import_button,
    threshold_label,
    threshold_input,
    threshold_value,
    fade_in_label,
    fade_in_input,
    fade_out_label,
    fade_out_input,
    normalize_button,
    export_button
]

for i, button in enumerate(buttons):
    button.grid(row=1, column=i, sticky="NSEW")
    button.configure(bg="#222", fg="#FFF", activebackground="#333", bd=1)

#threshold_input.configure(buttonbackground="#333", insertbackground="white")
fade_in_input.configure(buttonbackground="#333", insertbackground="white")
fade_out_input.configure(buttonbackground="#333", insertbackground="white")


# Configure grid
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(main_frame, 0, weight=1)
tk.Grid.columnconfigure(main_frame, 0, weight=1)
tk.Grid.columnconfigure(info_frame, 0, weight=1)
tk.Grid.columnconfigure(button_frame, list(range(len(buttons))), weight=1)


root.mainloop()