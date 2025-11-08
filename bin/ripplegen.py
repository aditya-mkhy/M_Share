from PIL import Image, ImageDraw

images = []

width = 200
center = width // 2
color_1 = (12, 87, 248,10)
color_2 = (255, 255, 255, 255)
max_radius = int(center * 1.5)
step = 8


for i in range(100, max_radius, step):
    im = Image.new('RGBA', (width+100, width+100), color_2)
    draw = ImageDraw.Draw(im)
    draw.ellipse(((center+50) - i, (center+50) - i, (center+50) + i, (center+50) + i), fill=color_1)
    images.append(im)

images[0].save('C:/Users/mahad/Downloads/pillow_imagedraw.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=60, loop=0)
