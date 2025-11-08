from PIL import Image, ImageTk
import os

path = "C:/Users/mahad/Downloads/Animation"

# avt = Image.open("C:/Users/mahad/Desktop/MShare2/data/avatar2/001.png")
images = []
n=0
for imgPath in os.listdir(path):
    print(f"{n}){imgPath}")
    fpath = f"{path}/{imgPath}"
    im = Image.open(fpath)
    # im.paste(avt, (24,18), mask = avt)
    images.append(im)


imLen = len(images)
print(imLen)
images[0].save('C:/Users/mahad/Downloads/senderRipple.gif',
                save_all=True, append_images=images, optimize=False, duration=40, loop=0)