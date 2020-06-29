from PIL import Image

img = Image.open('./11.jpg')

print(img.size)


img_resize = img.resize((413,626))
img_resize.show()
img_resize.save('chenzhiyin.jpg')