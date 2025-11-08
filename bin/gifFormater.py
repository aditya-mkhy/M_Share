from PIL import Image, ImageTk
path = "C:/Users/mahad/Downloads/scroll-animate-arrows.gif"
im = Image.open(path)
images = []
print(im.is_animated)
print(im.n_frames)

width, height = im.size

left = 250
top = 90
right = (width//2)+50
bottom = (height//2)+70

duration = im.info['duration']
print(duration)

for frame in range(0,im.n_frames):
    im.seek(frame)
    im1 = im.crop((left, top, right, bottom))
    im1 = im1.rotate(180)

    im1 = im1.convert("RGBA")

    data = im1.getdata()
    new_image_data = []

    for item in data:

        if item == (0, 0, 0):
            new_image_data.append((6, 6, 6))

        else:
            new_image_data.append(item) 
        

    im1.putdata(new_image_data)
    images.append(im1)


imLen = len(images)
images[0].save('C:/Users/mahad/Downloads/arrow.gif',
                save_all=True, append_images=images[1:imLen-5], optimize=False, duration=duration, loop=0)