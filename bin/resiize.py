p = r"D:\Projects\VideoDownloader\data\openf.png"

# Importing Image class from PIL module
from PIL import Image
 
# Opens a image in RGB mode
im = Image.open(p)
 
# Size of the image in pixels (size of original image)
# (This is not mandatory)
width, height = im.size

print(width, height)
 
width = int( width//1.8 )
height = int( height//1.8)

newsize = (40, 40)
print(newsize)

im1 = im.resize(newsize, Image.LANCZOS)

im1.save( r"D:\Projects\VideoDownloader\data\open.png")
im1.show()


# width = int( width//2 )
# height = int( height//2)

# newsize = (width, height)

# im1 = im.resize(newsize, Image.LANCZOS)
# # Shows the image in image viewer
# im1.show()
# im1.save("C:/Users/mahad/Downloads/logo-no-background2.png")