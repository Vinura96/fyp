from PIL import Image, ImageFilter

image = Image.open('done.jpg')
new_image = image.resize((250, 250))
new_image.save('image_250.jpg')
