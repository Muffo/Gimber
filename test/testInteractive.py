#-------------------------------------------------------------------------------
# Name:        modulo1
# Purpose:
#
# Author:      GrandiAn
#
# Created:     17/09/2013
# Copyright:   (c) GrandiAn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest
# from gimber.interactive import run as irun

import subprocess
import os
import signal
import urllib2

class TestGeneralCom(unittest.TestCase):

##    def setUp(self):
##        log = open('testInteractiveLog.txt', 'w')
##
##        self.serverProc = subprocess.Popen('python -m gimber interactive',
##                                stdout=log, stderr=log, shell=True)


    def testResponse(self):

        data = "SampleData"
        response = urllib2.urlopen('http://localhost:8080/echo/' + data)
        self.assertEqual(data, response.read())


##    def tearDown(self):
##        # os.kill(self.serverProc.pid, signal.SIGINT)
##        print "Executing this"
##        self.serverProc.terminate()



if __name__ == '__main__':
    unittest.main()
