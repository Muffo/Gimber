""" Paths that can be showed on the display as vector overlays
"""

import cv2
import numpy as np


class Path(object):
    """An abstract class that contains options and constants shared between vector overlays (Polygon, Polyline, Circle)
    """
    def __init__(self, options={}, extras={}):
        # Here I could add some validation
        if type(options) is not dict:
            raise ValueError("Options must be a dictionary")
        if type(extras) is not dict:
            raise ValueError("Extras must be a dictionary")

        self._options = options
        self._extras = extras


    @property
    def ptype(self):
        """ The Path type used in the dictionaries
        """
        return type(self).ptype

    @property
    def options(self):
        return self._options

    @property
    def dict(self):
        return {
            'ptype': self.ptype
        }

    @classmethod
    def checkDictPtype(cls, d):
        """ Check whether the ptype of the dictionary matches the ptype of the class
        """
        if not d.has_key('ptype'):
            raise ValueError("The dictionary for the Path does not contain the ptype")

        if d['ptype'] != cls.ptype:
            raise ValueError("Path type (ptype) does not match: %s != %s" %
                                                        (d['ptype'], cls.dtype))



class Marker(Path):
    """ A marker that is positioned in a precise point of the image

    :param point: a tuple/list of 2 elements (coordinates of the point)
    """
    def __init__(self, point, options={}):
        super(Marker, self).__init__(options)
        if len(point) != 2:
            raise ValueError("Invalid point: %s", (point))
        self._point = [float(point[0]), float(point[1])]

    ptype = 'marker'

    @classmethod
    def fromDict(cls, d):
        cls.checkDictPtype(d)
        if not d.has_key('point'):
            raise KeyError("Marker requires 'point': marker point coordinates")

        if d.has_key('options'):
            return Marker(d['point'], d['options'])
        else:
            return Marker(d['point'])

    @property
    def point(self):
        return self._point

    @property
    def dict(self):
        return {
            'ptype': self.ptype,
            'point': self._point,
            'options': self._options
        }



class Line(Path):
    """ A line between two points

    :param points: 2 points (es: [[x1, y1], [x2, y2]] )
    """
    def __init__(self, points, options={}):
        super(Line, self).__init__(options)

        if len(points) != 2:
            raise ValueError("Line must use exactly two points")

        for pt in points:
            if len(pt) != 2:
                raise ValueError("Invalid point: %s", (pt))


        self._points = [[float(points[0][0]), float(points[0][1])],
                        [float(points[1][0]), float(points[1][1])]]

        if self._points[0][0] == self._points[1][0] and \
            self._points[0][1] == self._points[1][1]:
            raise ValueError("The points of a line cannot be coincident")

    ptype = 'line'

    @classmethod
    def fromDict(cls, d):
        cls.checkDictPtype(d)
        if not d.has_key('points'):
            raise KeyError("Line requires 'points': list of 2 points coordinates")

        if d.has_key('options'):
            return Line(d['points'], d['options'])
        else:
            return Line(d['points'])


    @property
    def points(self):
        return self._points

    @property
    def dict(self):
        return {
            'ptype': self.ptype,
            'points': self._points,
            'options': self._options
        }



class PathParser(object):
    """ Utility class used to parse a dictionary that represents a path
    """
    paths = [Marker, Line]

    @staticmethod
    def fromDict(d):
        for path in PathParser.paths:
            if path.ptype == d['ptype']:
                return path.fromDict(d)

        raise ValueError("The dictionary does not correspond to any action")
