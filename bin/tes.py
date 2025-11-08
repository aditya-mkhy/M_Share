# Importing Image class from PIL module
from PIL import Image
 
# Opens a image in RGB mode
im = Image.open("C:/Users/mahad/Downloads/shot1.png")
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size
 
# Setting the points for cropped image
left = 0
top = 0
right = width//2
bottom = height
 
# Cropped image of above dimension
# (It will not change original image)
im1 = im.crop((left, top, right, bottom))
 
# Shows the image in image viewer
im1.show()

left = width//2
top = 0
right = width
bottom = height

im2 = im.crop((left, top, right, bottom))
im2.show()
