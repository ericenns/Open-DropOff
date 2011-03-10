#!/usr/bin/python
#COMMENT!!!!
from socket import *



myHost = ''             # me
myPort = 30000           # arbitrary port
myFile = "sentReadme"   # file to write to

f = open(myFile,"wb")
s = socket( AF_INET, SOCK_STREAM )
s.bind((myHost,myPort))
s.listen(5)

while 1:
    connection, address = s.accept()
    print address
    while 1:
        data = connection.recv(1024)            # receive data from client
        if data:
            f.write(data)                       # write to file
            connection.send('echo -> ' + data)  # echo for confirmation
        else:
            break
    f.close()
    connection.close()
