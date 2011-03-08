import sys
from socket import *

serverHost = '127.0.0.1'          # servername is localhost
serverPort = 30000                 # use arbitrary port > 1024
fileName = "README"               # read in file

#send file to server
def sendFile():
    f = open(fileName,"rb")
    for line in f:
        s.send(line)
    f.close()

s = socket( AF_INET, SOCK_STREAM )  # create a TCP socket

s.connect((serverHost, serverPort)) # connect to server on the port
sendFile()                          # send the data
data = s.recv(1024)                 # receive up to 1K bytes

print data

