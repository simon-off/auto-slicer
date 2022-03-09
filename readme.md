# Auto Slicer

#### Video Demo: <URL HERE>

## Description:

**Auto Slicer** is a Python GUI application designed to split up long audio files into smaller slices by detecting silence.

### Dependencies:

- **Tkinter** - Used for the GUI
- **PyDub** - Used for audio import/export and manipulation
- **MatPlotLib** - Used for waveform visualization of audio file
- **Numpy** - Used to interpolate numbers
- **Math** - used to convert wave file int values to dBFS
- **Path** - used to get the filename of imported sample

### Background:

I'm a music producer by trade and I wanted to create a tool that was relevant to my field of work. I often record samples to use in my production and this tool can help by taking long recordings with a few good moments and removing the "bloat", so to speak. Let's say I record a dog barking. There may be 5 seconds of barking in a 2 minute audio file. Run it through **Auto Slicer** and you're left with just the good stuff!

### Files:

- **app.py** is the main python application for the program. With just about 300 lines of code I decided to keep it all in one app.py file. Most of the lines are dedicated to drawing the UI using tKinter.

- **waveform.mplstyle** is a stylesheet file used by MatPlotLib to configure the look of the waveform visualization of the loaded audio file.

- **icon.ico** is a simple icon file for Tkinter.

- **app.exe** is a windows executable file of the program.

### How to use Auto Slicer:

1. Click **Import** and chose an audio file for slicing. This creates a new PyDub.AudioSegment object with the imported audio file and converts it to a 16Bit wav for further manipulation. It then calls the plot_waveform() function and draws a waveform visualization with the help of MatPlotLib.
2. Choose the **Threshold** for silence. This usually works best at low numbers for most audio files. This also renders the threshold as a line on top of the waveform by using Tkinter canvas.
3. Choose the **Padding**. This parameter decides how much silence to keep before and after each slice of audio. If you wan't tight slices with no "bloat" this is kept short. For longer audio with swelling sounds it's recommended to add a healthy amount of padding to prevent unintentional removal of quiet starts/ends.
4. Choose the **Fade In**. This fades each slice in by the chosen time in milliseconds.
5. Choose the **Fade Out**. This fades each slice out by the chosen time in milliseconds.
6. The **Tight** option changes how long of a silence is needed before it creates a new slice. For example on dialogue: Tight ON will tend to slice between each word and Tight OFF tend to slice between sentences instead. Tight mode is very useful for stuff like drums.
7. The **Normalize** option normalizes each slice to -0.1 dBFS by a built-in PyDub function. Use this if you want all your slices to be of similar volume.
8. Click **Export** when you're done dialing in the settings. This calls the export_file() function which uses the values from the other controls to slice up the imported audio file, process each slice (fades/normalization) and export them to a folder of your choosing. This function also converts the current threshold value into dBFS for use with PyDubs split_on_silence() function. A label with the export status is displayed in the gui. When the export is finished this tells the user how many slices were made.

### Design And Problems:

This project would not have been possible without the Tkinter library. Most of the lines of code are dedicated to configuring and drawing tkinter widgets to screen. It wasn't without some problems along the way but I got there in the end. I chose to go with a dark theme for the visual presentation since most of the music software I use has a similar aesthetic.

At first I tried to implement my own split_on_silence function but passing the correct data to and from PyDub in order to import/export the audio files proved to be too much of a hassle. PyDubs implementation of this feataure works great but it seems to detect the audio based on rms-values whereas I wanted the peak-value. In the end this is a minor detail and the remedy is simply to use a slightly lower threshold value to compensate. No biggie!

In the end I am proud to have created an application which I can see myself actually using! I'm gonna send it to some of my music producer friends as well and see what they think. Thank you CS50x for the knowledge and motivation to do this.

Written by: _Simon_
