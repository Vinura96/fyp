import numpy as np
from numpy import array,uint8
from PIL import Image, ImageFilter

im1 = Image.open("done.jpg")
xx=np.array(im1)



res = repr(xx) 
print(res[200:400])
eval(res)
print(eval(res))
