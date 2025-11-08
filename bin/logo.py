from tkinter import *
import ctypes , os , sys , socket
from random import choice , randint
from tkinter.filedialog import  askopenfilenames , askdirectory 
import tkinter.ttk as ttk
from threading import Thread
import time
from functools import partial as functools_partial

def resource_path(relative_path):
    path=os.path.dirname(sys.executable)    
    return path+'/'+relative_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def bouble_click_lab_wid(event=None):
    global lab_x,lab_y
    lab_x=event.x
    lab_y=event.y

def move_feedback_win(event=None):
    global scrn , lab_x,lab_y
    w=(scrn.winfo_geometry()).split('+')
    scrn.geometry(('+'+str((int(w[1])+event.x-lab_x))+'+'+str((int(w[2])+event.y)-lab_y)))



ctypes.windll.shcore.SetProcessDpiAwareness(1)

scrn = Tk()
bg = "pink4"
scrn.geometry('+924+720')
scrn.config(bg=bg)
userImg = PhotoImage(file =resource_path("data/avatar2/001.png"), master=scrn)
lab_x=0
lab_y=0
UserIcon = Label(scrn, highlightbackground=bg, image=userImg,fg=bg,
                bd=0,compound='right', cursor='hand2', bg=bg)

UserIcon.pack(side='top')

scrn.bind('<B1-Motion>',move_feedback_win)
scrn.bind('<Button-1>', bouble_click_lab_wid)
# scrn.wm_attributes('-alpha',0.8)

scrn.wm_attributes('-transparentcolor', bg)
scrn.config(bg=bg, bd=0, relief='raised')
scrn.attributes("-topmost", 1)
scrn.overrideredirect(True)


scrn.mainloop()
