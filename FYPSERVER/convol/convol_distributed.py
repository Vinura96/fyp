import socket
import time
import numpy as np
import pygame as game
from numpy import array,uint8
from PIL import Image, ImageFilter  
import base64  
from io import BytesIO


HOST = ''
PORT = 50007
procno = 2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(procno - 1) #Listens for (n) number of client connections
addr_list = []
datax=[]
print ('Waiting for client...')


for i in range(procno - 1): #Connects to all clients
    conn, addr = s.accept() #Accepts connection from client
    print ('Connected by', addr)
    addr_list.append(addr) #Adds address to address list


im1 = Image.open("image_300.jpg")    

w,h = im1.size
top= im1.crop((0, 0, w, int(h/2)))
buttom=im1.crop((0, int(h/2), w, h))

buffered = BytesIO()
#buttom.save(buffered, format="JPEG")
im1.save(buffered, format="JPEG")
img_str = base64.b64encode(buffered.getvalue())
datax.append(img_str)
start=time.time()
for i in range(procno - 1): #Converts array section into string to be sent
    arraystringx = repr(datax)

    conn.sendto( arraystringx.encode('utf_8'), addr_list[i] ) #Sends array string

#topx = top.filter(ImageFilter.Kernel((3, 3), (0, 0, 0, 0, 1, 0, 0, 0, -1), 1, 0))

for i in range(procno - 1): #Receives sorted sections from each client

    arraystring = ''
    while 1:
        data = conn.recv(4096) #Receives data in chunks
        arraystring += data.decode('utf_8') #Adds data to array string
        if ']' in data.decode('utf_8'): #When end of data is received
            break
        
im_bytes = base64.b64decode(eval(arraystring)[0])   # im_bytes is a binary image
im_file = BytesIO(im_bytes)  # convert image to file-like object
buttomx = Image.open(im_file)

##def get_concat_v(im1, im2):
##    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
##    dst.paste(im1, (0, 0))
##    dst.paste(im2, (0, im1.height))
##    return dst
##new=get_concat_v(topx, buttomx)
print(time.time()-start)
print("finished")
#new.save("final.jpg")  

conn.close()

