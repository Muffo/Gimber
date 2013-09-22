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
from numpy.testing import assert_array_equal
from gimber.display import *


class AbstractDisplayTests(unittest.TestCase):
    """Contains tests that can be done both for LocalDisplay and RemoteDispla"""
    def addPaths(self, display):
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 0)

        actions = display.actionsFrom(1)
        self.assertEqual(len(actions), 0)

        display.addMarker([10, 10])
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 1)

        actions = display.actionsFrom(1)
        self.assertEqual(len(actions), 0)

        display.addMarker([12, 12])
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 2)

        actions = display.actionsFrom(1)
        self.assertEqual(len(actions), 1)

    def clear(self, display):
        display.addMarker([10, 10])
        display.addMarker([12, 12])
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 2)
        self.assertIsInstance(actions[0], AddPaths)
        self.assertIsInstance(actions[1], AddPaths)

        display.clear()
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 3)
        self.assertIsInstance(actions[0], EmptyAction)
        self.assertIsInstance(actions[1], EmptyAction)
        self.assertIsInstance(actions[2], ClearPaths)


class LocalDisplayTests(AbstractDisplayTests):

    def testAddPaths(self):
        display = LocalDisplay()
        self.addPaths(display)


    def testLoadImage(self):
        display = LocalDisplay()
        # Create a syntethic random image
        image = np.array(np.random.rand(3, 4) * 256, dtype=np.uint8)
        display.loadImage(image)
        assert_array_equal(display.tileCreator.image, image)

        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 1)
        self.assertIsInstance(actions[0], LoadImage)

        image = np.array(np.random.rand(3, 4) * 256, dtype=np.uint8)
        display.loadImage(image)
        assert_array_equal(display.tileCreator.image, image)

        # Now the previous load image action should be an EmptyAction
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 2)
        self.assertIsInstance(actions[0], EmptyAction)
        self.assertIsInstance(actions[1], LoadImage)


    def testClear(self):
        display = LocalDisplay()
        self.clear(display)


    def testDict(self):
        display = LocalDisplay()
        display.addMarker([10, 10])
        display.addMarker([12, 12])
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0].dict['atype'], 'addpaths')
        self.assertEqual(len(actions[0].dict['paths']), 1)
        self.assertEqual(actions[0].dict['paths'][0]['ptype'], 'marker')


class RemoteDisplayManagerTests(unittest.TestCase):
    def testCreateDelete(self):
        rdm = RemoteDisplayManager("http://localhost:8080")

        displayId1 = "disp1"
        displayId2 = "disp2"

        rdm.create("disp1")
        rdm.create("disp2")
        self.assertRaises(ServerSideError, rdm.create, "disp1")
        self.assertRaises(ServerSideError, rdm.create, "disp2")

        rdm.delete("disp1")
        rdm.delete("disp2")
        self.assertRaises(ServerSideError, rdm.delete, "disp1")
        self.assertRaises(ServerSideError, rdm.delete, "disp2")


class RemoteDisplayTests(AbstractDisplayTests):

    def testAddPaths(self):
        rdm = RemoteDisplayManager("http://localhost:8080")
        display = rdm.create("disp1")
        self.addPaths(display)
        rdm.delete("disp1")

    def testClear(self):
        rdm = RemoteDisplayManager("http://localhost:8080")
        display = rdm.create("disp1")
        self.clear(display)
        rdm.delete("disp1")



if __name__ == '__main__':
    unittest.main()
