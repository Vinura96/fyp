import socket
import time


HOST = ''
PORT = 50007
procno = 2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(procno - 1) #Listens for (n) number of client connections
addr_list = []
data=[]
print ('Waiting for client...')


for i in range(procno - 1): #Connects to all clients
    conn, addr = s.accept() #Accepts connection from client
    print ('Connected by', addr)
    addr_list.append(addr) #Adds address to address list

data.append(time.time())
      
for i in range(procno - 1): #Converts array section into string to be sent
    arraystring = repr(data)
    conn.sendto( arraystring.encode('utf_8') , addr_list[i] ) #Sends array string


for i in range(procno - 1): #Receives sorted sections from each client

    arraystring = ''
    while 1:
        data = conn.recv(4096) #Receives data in chunks
        arraystring += data.decode('utf_8') #Adds data to array string
        if ']' in data.decode('utf_8'): #When end of data is received
            break
    
print(time.time()-eval(arraystring)[0])


conn.close()

