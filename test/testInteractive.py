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
import os
import subprocess
import signal
import json
import urllib3
import requests

class TestInteractive(unittest.TestCase):

    def setUp(self):
        self.baseUrl = 'http://localhost:8080'
        self.createUrl = self.baseUrl + '/create'
        self.deleteUrl = self.baseUrl + '/delete'
        self.doUrl = self.baseUrl + '/do'
        self.actionsUrl = self.baseUrl + '/actions'
        self.session = requests.Session()
##        log = open('testInteractiveLog.txt', 'w')
##
##        self.serverProc = subprocess.Popen('python -m gimber interactive',
##                                stdout=log, stderr=log, shell=True)


    def getJsonUrllib2(self, url, dataDict):
        import urllib2
##        data = urllib.urlencode(values)
        data = json.dumps(dataDict)
        request = urllib2.Request(url, data)
        response = urllib2.urlopen(request)
        return json.loads(response.read())

    def getJson(self, url, dataDict, expectedCode=200):
        r = self.session.post(url, data=json.dumps(dataDict))
        self.assertEqual(r.status_code, expectedCode)
        return r.json()


    def testCreateDelete(self):
        displayId1 = {"displayId": "disp1"}
        displayId2 = {"displayId": "disp2"}

        response = self.getJson(self.createUrl, displayId1)
        self.assertEqual(response['result'], "ok")
        response = self.getJson(self.createUrl, displayId2)
        self.assertEqual(response['result'], "ok")
        response = self.getJson(self.createUrl, displayId1)
        self.assertEqual(response['result'], "error")

        response = self.getJson(self.deleteUrl, displayId1)
        self.assertEqual(response['result'], "ok")
        response = self.getJson(self.deleteUrl, displayId2)
        self.assertEqual(response['result'], "ok")
        response = self.getJson(self.deleteUrl, displayId1)
        self.assertEqual(response['result'], "error")


    def testDoAddPaths(self):
        displayId1 = {"displayId": "disp1"}

        action = {
            'atype': 'addpaths',
            'paths': [
                {
                    'ptype': 'marker',
                    'point': [10, 12]
                },
                {
                    'ptype': 'line',
                    'points': [[10, 12], [13, 15]]
                }
            ]
        }

        response = self.getJson(self.createUrl, displayId1)
        self.assertEqual(response['result'], "ok")

        response = self.getJson(self.doUrl + "/disp1", action)
        self.assertEqual(response['result'], "ok")

        response = self.session.get(self.actionsUrl + "/disp1/0").json()
        self.assertEqual(response['result'], "ok")
        self.assertEqual(response['actions'][0]['atype'], 'addpaths')


        response = self.getJson(self.deleteUrl, displayId1)
        self.assertEqual(response['result'], "ok")



##    def tearDown(self):
##        # os.kill(self.serverProc.pid, signal.SIGINT)
##        print "Executing this"
##        self.serverProc.terminate()



if __name__ == '__main__':
##    import cProfile
##    cProfile.run("unittest.main()")

    unittest.main()
