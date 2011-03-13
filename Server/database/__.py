'''
Created on 2011-03-10

@author: Mike
'''

from UsersDB import *

x = UsersDB()

x.connect()
#x.createTable()
#x.deleteTable()
#data = x.getAllUser()

#x.addUser("user1","123")
#x.removeUser("user1")
result = x.authenticate("user2","234")
print result

#x.addFile("user2" , "1", "file_1", "c:/samplefolder/file_1.html","user2","1")
#x.addFile("user2" , "2", "file_2", "c:/samplefolder/file_2.html","user2","1")
fileinfo = x.getFile("user2","c:/samplefolder/file_1.html")
print fileinfo

files = x.getFiles("user2")
print files
x.disconnect()
#print data