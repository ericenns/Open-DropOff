import unittest
from UsersDBTest import *
from FilesDBTest import *

UsersDBTestCase = unittest.TestLoader().loadTestsFromTestCase(UsersDBTest)
FilesDBTestCase = unittest.TestLoader().loadTestsFromTestCase(FilesDBTest)
unittest.TextTestRunner(verbosity=2).run(UsersDBTestCase)
unittest.TextTestRunner(verbosity=2).run(FilesDBTestCase)