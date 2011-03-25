'''
Created on Mar 24, 2011

@author: Andrew
'''

try: 
    from hashlib import sha1
    sha_constructor = sha1
except ImportError:
    import sha
    sha_constructor = sha.new


class AccountHandler(object):
    '''
    classdocs
    '''

    def __init__(self, conn):
        '''
        Constructor
        '''
        self.connHandler = conn
    
    def createNewUser(self, arguments):
        newuser, newpass = arguments.split("\r\n")
        print "New user: %s" % newuser
        print "new pass: %s" % newpass
        
        #conn = DatabaseConnection()
        #conn.connect("localhost", "username", "password", "open-dropoff")
        #udb = UsersDB(conn)
        
        #nameTaken = udb.userExists(newuser)
        #if not nameTaken:
        #    meetsReq = checkPassReq(newpass)
        #    if meetsReq:
        #        udb.addUser( newuser, newpass )
        #        self.connHandler.send("STAT 100")
        #    else:
        #        self.connHandler.send("STAT 204")
        #else:
        #    print "Name taken, try again!"
        #    self.connHandler.send("STAT 203")
        
        #conn.disconnect()
            

    def changePassword(self, arguments):
        password, key = arguments.split("\r\n")
        print "in changePassword password: %s" % password
        print "in changePassword key: %s" % key
        
        #verify key
        if(key == "45f106ef4d5161e7aa38cf6c666607f25748b6ca"):
            self.connHandler.send("STAT\r\n100")
        else:
            self.connHandler.send("STAT\r\n200")
            return
    
    def checkPassReq(self, newpass):
        if len(newpass) > 8:
            return True
        else:
            return False
        
    def login(self, arguments):
        username = arguments
        print "User: %s" % username
        #conn = DatabaseConnection.DatabaseConnection()
        #conn.connect(DBHOST, DBUSER, DBPASS, DB)
        #udb = UsersDB.UsersDB(conn)
        
        #validUser = udb.userExists(username)
        
        #if(validUser):
        if(username == "user"):
            self.connHandle.send("STAT\r\n100")
            self.data = self.connHandler.recv()
            command, arguments = self.data.split("\r\n", 1)
            
            if(command == "PASS"):
                password = arguments
                
                #validPass = udb.authenticate(username, password)
                #if(validPass):
                if(password == "pass"):
                    key = sha_constructor("%s%s" % (username, password)).hexdigest()
                    self.connHandler.send("STAT\r\n100\r\n%s" % key)
                else:
                    self.connHandler.send("STAT\r\n202")
            else:
                #not sure if this is needed
                self.connHandler.send("FAIL")
        else:
            self.connHandler.send("STAT\r\n201")
            
        #conn.disconnect()
            
        