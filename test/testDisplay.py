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


class DisplayTests(unittest.TestCase):

    def testAddPaths(self):
        display = Display()
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


    def testLoadImage(self):
        display = Display()
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
        display = Display()
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


    def testDict(self):
        display = Display()
        display.addMarker([10, 10])
        display.addMarker([12, 12])
        actions = display.actionsFrom(0)
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions[0].dict['atype'], 'addpaths')
        self.assertEqual(len(actions[0].dict['paths']), 1)
        self.assertEqual(actions[0].dict['paths'][0]['ptype'], 'marker')



if __name__ == '__main__':
    unittest.main()
