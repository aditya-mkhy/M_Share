import pyscreenshot as ImageGrab
from time import sleep


    
# n = 0

# def on_press(key):
    
#     if key == keyboard.Key.enter:
#         global n
#         img = ImageGrab.grab(bbox=(129,282, 352,352))
#         n+=1
#         filepath = f"C:/Users/mahad/Documents/ScreenShot/shot{n}.png"
#         img.save(filepath)
#         img.show()
   


# # Collect events until released
# with keyboard.Listener(
#         on_press=on_press) as listener:
#     listener.join()

# # ...or, in a non-blocking fashion:
# listener = keyboard.Listener(
#     on_press=on_press)
# listener.start()


# from time import sleep

import pyautogui


# while True:
#     print(pyautogui.position())
#     sleep(1)



while True:
    p = input("Enter cords : ")
    x, y = p.split(" ")
    x = int(x.strip())
    y = int(y.strip())
    img = ImageGrab.grab(bbox=(1194,203, 1308,250))#1320  248
    filepath = f"C:/Users/mahad/Documents/but2.png"
    img.save(filepath)
    img.show()
    break


