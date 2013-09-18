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
from gimber.paths import *

class PathTests(unittest.TestCase):
    def testMarker(self):
        self.assertRaises(TypeError, Marker, 1)
        self.assertRaises(ValueError, Marker, [])
        self.assertRaises(ValueError, Marker, [1])
        self.assertRaises(ValueError, Marker, [1, 2, 3])
        self.assertEqual(Marker(["1.1", 2]).point[0], 1.1)

    def testLine(self):
        self.assertRaises(TypeError, Line, 1)
        self.assertRaises(ValueError, Line, [])
        self.assertRaises(TypeError, Line, [1, 1])
        self.assertRaises(ValueError, Line, [[1, 2], [3]])
        self.assertRaises(ValueError, Line, [[1, 2], [3, 3], [4, 5]])
        self.assertRaises(ValueError, Line, [[1.1, 2], [1.1, 2]])
        self.assertRaises(ValueError, Line, [["1.1", 2], [1.1, 2]])
        self.assertEqual(Line([["1.1", 2], [2, 4]]).points[0][0], 1.1)


class PathParsingTests(unittest.TestCase):
    def testDict(self):
        marker = PathParser.fromDict({
            'ptype': 'marker',
            'point': [10, 12]
        })
        self.assertIsInstance(marker, Marker)

        line = PathParser.fromDict({
            'ptype': 'line',
            'points': [[10, 12], [13, 15]]
        })
        self.assertIsInstance(line, Line)

        self.assertRaises(KeyError, PathParser.fromDict, {
            'ptype': 'line',
            'point': [[10, 12], [13, 15]]
        })

        self.assertRaises(KeyError, PathParser.fromDict, {
            'ptype': 'marker',
            'points': [10, 12]
        })


if __name__ == '__main__':
    unittest.main()

