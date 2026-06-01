import socket


HOST = '192.168.1.38'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


#Receives arraystring in chunks
arraystring = ''

while 1:

    data = s.recv(4096) #Receives data in chunks
    #print data
    arraystring += data.decode('utf_8') #Adds data to array string
    if ']' in data.decode('utf_8'): #When end of data is received

        break
array = eval(arraystring)



#Converts array into string to be sent back to server
arraystring = repr(array)
s.sendall(arraystring.encode('utf_8')) #Sends array string


s.close()




