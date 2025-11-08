from PIL import Image

path = "C:/Users/mahad/Downloads/arrow.gif"
img = Image.open(path)
img.seek(10)

img = img.convert("RGB")
datas = img.getdata()
new_image_data = []
n = 0
for item in datas:

    if item == (0, 0, 0):
        new_image_data.append((6, 6, 6))

    else:
        new_image_data.append(item) 
      

img.putdata(new_image_data)
img.show()