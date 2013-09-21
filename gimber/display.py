#-------------------------------------------------------------------------------
# Name:        modulo1
# Purpose:
#
# Author:      GrandiAn
#
# Created:     09/09/2013
# Copyright:   (c) GrandiAn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from tiles import *
from actions import *
from paths import *

class Display(object):
    def __init__(self):
        self._tileCreator = None
        self._actions = []

    @property
    def tileCreator(self):
        return self._tileCreator

    @property
    def actions(self):
        return self._actions

    def actionsFrom(self, last):
        return self._actions[last:]

    def _replaceActions(self, oldActionType, newActionType):
        for i, action in enumerate(self._actions):
            if isinstance(action, oldActionType):
                self._actions[i] = newActionType()

    def do(self, action):
        if isinstance(action, ClearPaths):
            self._replaceActions(AddPaths, EmptyAction)

        if isinstance(action, LoadImage):
            self._replaceActions(LoadImage, EmptyAction)
            self._tileCreator = TileCreator(action.image)

        self._actions.append(action)


    def addMarker(self, point, options={}):
        marker = Marker(point, options)
        action = AddPaths([marker])
        self.do(action)


    def addLine(self, points, options={}):
        line = Line(points, options)
        action = AddPaths([line])
        self.do(action)


    def clear(self):
        action = ClearPaths()
        self.do(action)


    def loadImage(self, image):
        action = LoadImage(image)
        self.do(action)
