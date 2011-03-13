'''
Created on 2011-03-10

@author: Mike
'''

from UsersDB import *

x = UsersDB()

x.connect()
x.createTable()
#x.deleteTable()
#data = x.getAllUser()
x.disconnect()
#print data