import time
import numpy as np

from PIL import Image, ImageFilter  
  
im1 = Image.open("image_250.jpg")
timestart=time.time()
im2 = im1.filter(ImageFilter.Kernel((3, 3), 
          (0, 0, 0, 0, 1, 0, 0, 0, -1), 1, 0))  
print(time.time()-timestart)
    
