import time
import numpy as np
from numpy import array,uint8
from PIL import Image, ImageFilter  
import base64  
from io import BytesIO
import socket


HOST = '192.168.1.35'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

datax=[]
#Receives arraystring in chunks
arraystring = ''

while 1:

    data = s.recv(4096) #Receives data in chunks
    #print data
    arraystring += data.decode('utf_8') #Adds data to array string
    if ']' in data.decode('utf_8'): #When end of data is received

        break

im_bytes = base64.b64decode(eval(arraystring)[0])   # im_bytes is a binary image
im_file = BytesIO(im_bytes)  # convert image to file-like object
im1 = Image.open(im_file)


buttom = im1.filter(ImageFilter.Kernel((3, 3), 
          (0, 0, 0, 0, 1, 0, 0, 0, -1), 1, 0))  

buffered = BytesIO()
buttom.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue())
datax.append(img_str)
arraystring = repr(datax)
s.sendall(arraystring.encode('utf_8')) #Sends array string


s.close()
