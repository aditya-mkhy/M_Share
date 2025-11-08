import pyscreenshot as ImageGrab
from pynput import keyboard
import pyautogui
from time import sleep


    
# while True:
#     print(pyautogui.position())
#     sleep(1)

cord = (1438,476, 1610,519)

img = ImageGrab.grab(bbox=cord)
filepath = f"C:/Users/mahad/Documents/ScreenShot/shot.png"
img.save(filepath)
img.show()