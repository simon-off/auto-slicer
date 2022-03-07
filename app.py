# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
# PyDub
from pydub import AudioSegment, silence
# MatPlotLib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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


# Exit program command
def quit_program():
    root.quit()
    root.destroy()


# Root window
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", quit_program)
root.title('Auto Slicer')
root.geometry("1320x280+300+300")
root.configure(bg="#191919")


# Import and load imput_sample to PyDub
def import_file():
    filetypes = (("Audio files", "*.wav *.mp3 *.aif *.ogg"),)
    global filepath
    filepath = filedialog.askopenfile(filetypes=filetypes).name

    global audio_file
    audio_file = AudioSegment.from_file(filepath)

    filepath_label.config(text=filepath)
    audio_length_label.config(text=str(round(audio_file.duration_seconds, 3)) + " SECONDS")
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
    canvas = FigureCanvasTkAgg(fig, master=wave_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, sticky="NSEW")
    canvas.get_tk_widget().configure(background="#000")

    # Add threshold line
    global line_canvas
    line_canvas = tk.Canvas(wave_frame)
    line_canvas.configure(bg="#0099FF", height=2, highlightthickness=0)
    line_canvas.place(relwidth=1)
    draw_lines()


# Update and draw Threshold Line
def draw_lines():
    if line_canvas:
        line_canvas.place_configure(rely=((threshold / -200) + 0.5 - 0.002))


# Command that runs when changing the threshold value
def update_threshold(value):
    threshold_value.config(text=value)
    global threshold
    threshold = int(value)
    draw_lines()


# Commands to update the fade_in/fade_out label
def update_fade_in(value):
    fade_in_value.config(text=value)
def update_fade_out(value):
    fade_out_value.config(text=value)


# Export Sliced Sample(s)
def export_file():
    if filepath:
        # calculate proper dbfs values for the split_on_silence function
        threshold_16 = numpy.interp(threshold, [0, 100], [1, 32768])
        valueDBFS = round(20 * math.log10(abs(threshold_16)/32768), 1)

        export_folder = filedialog.askdirectory()
        slices = silence.split_on_silence(audio_file, silence_thresh=valueDBFS)
        for i, slice in enumerate(slices):
            with open("{}/slice-{}.wav".format(export_folder, i), "wb") as f:
                slice.export(f, format="wav")


# Frame to draw graph and lines
wave_frame = tk.Frame(root, bg="#191919")
wave_frame.grid(row=0, sticky="NSEW")


# Frame for info row
info_frame = tk.Frame(root, bg="#111")
info_frame.grid(row=1, sticky="EW")
# Filepath label
filepath_label = tk.Label(info_frame, bg="#111", fg="#666", padx=6)
filepath_label.grid(sticky="W", row=0)
# Audio length label
audio_length_label = tk.Label(info_frame, bg="#111", fg="#666", padx=6)
audio_length_label.grid(sticky="E", row=0)


# Frame for button row
button_frame = tk.Frame(root, bg="#272727", bd=1, padx=6, pady=4)
button_frame.grid(row=2, sticky="SEW")
# Import widget
import_button = tk.Button(button_frame, text="Import", activeforeground="#AAA", command=import_file)
# Threshold widgets
threshold_label = tk.Label(button_frame, text="Threshold ", anchor="e")
threshold_input = tk.Scale(
    button_frame,
    troughcolor="#444",
    showvalue=False,
    orient=tk.HORIZONTAL,
    command=update_threshold,
    )
threshold_value = tk.Label(button_frame, text=0, anchor="w", width=1)
# Fade in widgets
fade_in_label = tk.Label(button_frame, text="Fade in ", anchor="e")
fade_in_input = tk.Scale(button_frame,
    troughcolor="#444",
    showvalue=False,
    orient=tk.HORIZONTAL,
    command=update_fade_in,
    )
fade_in_value = tk.Label(button_frame, text=0, anchor="w", width=1)
# Fade out widgets
fade_out_label = tk.Label(button_frame, text="Fade out ", anchor="e")
fade_out_input = tk.Scale(button_frame,
    troughcolor="#444",
    showvalue=False,
    orient=tk.HORIZONTAL,
    command=update_fade_out,
    )
fade_out_value = tk.Label(button_frame, text=0, anchor="w", width=1)
# Normalize widgets
normalize_button = tk.Checkbutton(button_frame, text="Normalize", selectcolor="#444", activeforeground="#AAA")
normalize_button.deselect()
# Export widget
export_button = tk.Button(button_frame, text="Export", activeforeground="#AAA", command=export_file)


# Draw Frame Widgets
buttons = [
    import_button,
    threshold_label,
    threshold_input,
    threshold_value,
    fade_in_label,
    fade_in_input,
    fade_in_value,
    fade_out_label,
    fade_out_input,
    fade_out_value,
    normalize_button,
    export_button
]


# Draw buttons with grid
for i, button in enumerate(buttons):
    button.grid(row=0, column=i, sticky="NSEW")
    button.configure(bg="#272727", fg="#FFF", activebackground="#333", bd=1, highlightthickness=0)


# Configure grid
tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)
tk.Grid.rowconfigure(wave_frame, 0, weight=1)
tk.Grid.columnconfigure(wave_frame, 0, weight=1)
tk.Grid.columnconfigure(info_frame, 0, weight=1)
tk.Grid.columnconfigure(button_frame, [0, 2, 5, 8, 10, 11], weight=3)
tk.Grid.columnconfigure(button_frame, [1, 3, 4, 6, 7, 9], weight=1)


root.mainloop()