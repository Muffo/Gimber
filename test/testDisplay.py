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
