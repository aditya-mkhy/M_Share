# Import the required libraries
from tkinter import *
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Create an instance of Tkinter Frame
root = Tk()
root.tk.call('tk', 'scaling',  0.0)

# Set the geometry
root.geometry("700x350")

# Create a Canvas with a background color
C = Canvas(root, bg="blue", height=500, width=600)

# Coordinates for the arc
coord = 50, 50, 400, 400

# Create the arc with extent=150
arc = C.create_arc(coord, start=90, extent=90, fill="red", dashoff=0, width=0)

C.pack(side=TOP, padx=50, pady=50)

root.mainloop()