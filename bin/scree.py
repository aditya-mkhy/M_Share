import pyscreenshot as ImageGrab
from pynput import keyboard
from time import sleep


    
n = 0

images = []

def save():
    global images, n
    print("Saving")
    for img in images:
        n+=1
        filepath = f"C:/Users/mahad/Documents/ScreenShot/shot{n}.png"
        img.save(filepath)
    print("DOne")


def on_press(key):
    bbox=(250,340, 755,830)
    
    if key == keyboard.Key.enter:
        for i in range(70):
            # part of the screen
            images.append( ImageGrab.grab(bbox))
        save()

    if key == keyboard.Key.shift_r:
        mg = ImageGrab.grab(bbox)
        mg.show()



   

# Collect events until released
with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press)
listener.start()


from time import sleep

import pyautogui
while True:
    print(pyautogui.position())
    sleep(1)