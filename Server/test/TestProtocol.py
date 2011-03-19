import unittest
import socket

try: 
   from hashlib import sha1
   sha_constructor = sha1
except ImportError:
   import sha
   sha_constructor = sha.new

class TestProtocol(unittest.TestCase):

    def setUp(self):
        self.key = "63e780c3f321d13109c71bf81805476e"
        self.username = "user"
        self.password = "pass"
        self.server = "localhost"
        self.port = 30000
        self.testFile = "test.txt"
        self.testFileSize = 84
        self.sendSize = 100
        self.receiveSize = 100
    
    def openConnection(self):
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect((self.server, self.port))
        return sock
        
    def closeConnection(self, sock):
        sock.send("CLOS\r\n")
        sock.close()
        
    def computeChecksum(self, file):
        file_hash = sha_constructor()
        
        line = file.read(128)
        while line:
            file_hash.update(line)
            line = file.read(128)
        
        return file_hash.hexdigest()
        
    def test_login(self):
        sock = self.openConnection()
        
        sock.send("USER\r\n%s" % self.username)
        response = sock.recv(80)
        self.assertEqual("OKAY", response)
        
        sock.send("PASS\r\n%s" % self.password)
        response = sock.recv(80)
        status = response[:4]
        self.assertEqual("OKAY", status)
        
        status, key = response.split("\r\n", 1)
        self.assertEqual(self.key, key)
        
        self.closeConnection(sock)
        
    def test_push(self):
        sock = self.openConnection()
        
        sock.send("PUSH\r\n%s\r\n%i\r\n%s" % (self.testFile, self.testFileSize, self.key))
        response = sock.recv(80)
        self.assertEqual("OKAY", response)
        
        file = open(self.testFile,"rb")
        line = file.read(self.sendSize)
        while line:
            sent = sock.send(line)
            while sent != len(line):
                sent += sock.send(line[sent:])
            line = file.read(self.sendSize)      
        file.close()
        response = sock.recv(80)
        self.assertEqual("OKAY", response)
        
        self.closeConnection(sock)
        
    def test_pull(self):
        sock = self.openConnection()
        
        sock.send("PULL\r\n%s\r\n%s" % (self.testFile, self.key))
        response = sock.recv(80)
        command = response[:4]
        self.assertEqual("RECV", command)
        
        command, fileSize = response.split("\r\n", 1)
        fileSize = int(fileSize)
        self.assertEqual(self.testFileSize, fileSize)
        
        sock.send("SEND")
        newfile = open("%s.test" % self.testFile, "wb")
        totalReceived = -1
        while totalReceived <= fileSize:
            if(totalReceived == -1):
                totalReceived == 0
            content = sock.recv(self.receiveSize)
            totalReceived = totalReceived + self.receiveSize
            newfile.write(content)
        newfile.close()
        
        file = open(self.testFile, "rb")
        file_digest = self.computeChecksum(file)
        file.close()
        testFile = open("%s.test" % self.testFile, "rb")
        testFile_digest = self.computeChecksum(testFile)
        testFile.close()
        self.assertEqual(file_digest, testFile_digest)
        
        self.closeConnection(sock)
    
if __name__ == '__main__':
    unittest.main()
