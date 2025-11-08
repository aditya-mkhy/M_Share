import pyscreenshot as ImageGrab
from pynput import keyboard
from time import sleep
import pyautogui

    
n = 0

path = f"C:/Users/mahad/Documents/ScreenShot/shot.png"

pos =  0
box = (112,293, 280,340)


if pos:
    while True:
        print(pyautogui.position())
        sleep(1)   

else:
    img = ImageGrab.grab(bbox=box)
    img.save(path)
    img.show()


