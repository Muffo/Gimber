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
import base64

import numpy as np
from numpy.testing import assert_array_equal

from gimber.actions import *
from gimber.paths import *

class ActionParsingTests(unittest.TestCase):

    def testAddPaths(self):
        addPathsDict = {
            'atype': 'addpaths',
            'paths': [
                {
                    'ptype': 'marker',
                    'point': [10.0, 12.0],
                    'options': {}
                },
                {
                    'ptype': 'line',
                    'points': [[10.0, 12.0], [13.0, 15.0]],
                    'options': {}
                }
            ]
        }

        addPathsAction = ActionParser.fromDict(addPathsDict)
        self.assertIsInstance(addPathsAction, AddPaths)
        self.assertIsInstance(addPathsAction.paths[0], Marker)
        self.assertIsInstance(addPathsAction.paths[1], Line)

        addPathsAction2 = AddPaths([Marker([10, 12]), Line([[10, 12], [13, 15]])])
        self.assertDictEqual(addPathsDict, addPathsAction2.dict)


    def testClearPaths(self):
        clearPathsAction = ActionParser.fromDict({
            'atype': 'clearpaths'
        })
        self.assertIsInstance(clearPathsAction, ClearPaths)


    def testEmptyAction(self):
        emptyAction = ActionParser.fromDict({
            'atype': 'empty'
        })
        self.assertIsInstance(emptyAction, EmptyAction)


    def testLoadImage(self):
        # Create a syntethic random image
        image = np.array(np.random.rand(3, 4) * 256, dtype=np.uint8)

        loadImageDict = {
             'atype': 'loadimage',
             'image': base64.b64encode(image),
             'shape': image.shape
        }

        loadImageAction = ActionParser.fromDict(loadImageDict)
        self.assertIsInstance(loadImageAction, LoadImage)
        assert_array_equal(loadImageAction.image, image)

        loadImageAction2 = LoadImage(image)
        self.assertDictEqual(loadImageAction2.dict, loadImageDict)


        self.assertRaises(KeyError, ActionParser.fromDict, {
            'atype': 'loadimage',
            'image': base64.b64encode(image),
        })

        self.assertRaises(KeyError, ActionParser.fromDict, {
            'atype': 'loadimage',
            'shape': image.shape
        })

        self.assertRaises(ValueError, ActionParser.fromDict, {
            'atype': 'loadimage',
            'image': base64.b64encode(image),
            'shape': (10, 11, 12)
        })




    def testNotExisting(self):
        self.assertRaises(ValueError, ActionParser.fromDict, {
            'atype': 'notvalid'
        })



if __name__ == '__main__':
    unittest.main()
