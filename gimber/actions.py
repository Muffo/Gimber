#-------------------------------------------------------------------------------
# Name:         actions
# Purpose:
#
# Author:       GrandiAn
#
# Created:      09/09/2013
# Copyright:    (c) GrandiAn 2013
# Licence:      <your licence>
#-------------------------------------------------------------------------------

import base64

import numpy as np

from paths import PathParser

class GenericAction(object):
    def __init__(self):
        pass

    @property
    def atype(self):
        return type(self).atype

    @property
    def dict(self):
        return {
            'atype': self.atype
        }

    @classmethod
    def checkDictAtype(cls, d):
        if d['atype'] != cls.atype:
            raise ValueError("Action type (atype) does not match: %s != %s" %
                                                        (d['atype'], cls.atype))

    @classmethod
    def fromDict(cls, d):
        cls.checkDictAtype(d)
        # TODO: check that there are no extra parameters in the dictionary
        return cls()


class AddPaths(GenericAction):
    def __init__(self, paths):
        # super(AddPaths, self).__init__()
        self._paths = paths

    atype = "addpaths"

    @property
    def paths(self):
        return self._paths

    @classmethod
    def fromDict(cls, d):
        cls.checkDictAtype(d)
        if not d.has_key('paths'):
            raise KeyError("AddPaths requires 'paths': a list of paths")
        paths = [PathParser.fromDict(pd) for pd in d['paths']]
        return AddPaths(paths)

    @property
    def dict(self):
        return {
            'atype': self.atype,
            'paths': [e.dict for e in self.paths]
        }


class ClearPaths(GenericAction):
##    def __init__(self):
##        super(ClearPaths, self).__init__()

    atype = "clearpaths"


class EmptyAction(GenericAction):
##    def __init__(self):
##        super(EmptyAction, self).__init__()

    atype = "empty"


class LoadImage(GenericAction):
    def __init__(self, image):
        # super(AddPaths, self).__init__()
        self._image = image

    atype = "loadimage"

    @property
    def image(self):
        return self._image

    @classmethod
    def fromDict(cls, d):
        cls.checkDictAtype(d)
        if not d.has_key('image'):
            raise KeyError("AddPaths requires 'paths': a list of paths")
        if not d.has_key('shape'):
            raise KeyError("AddPaths requires 'shape': [h, w] of the image")
        if len(d['shape']) != 2:
            raise ValueError("Unvalid format for AddPaths' parameter 'shape'")

        # TODO: add support for custom dtype
        imageBuffer = base64.decodestring(d['image'])
        image = np.frombuffer(imageBuffer, dtype=np.uint8)
        image.shape = d['shape']
        return LoadImage(image)



class ActionParser(object):

    actions = [AddPaths, ClearPaths, LoadImage, EmptyAction]

    @staticmethod
    def fromDict(d):
        for action in ActionParser.actions:
            if action.atype == d['atype']:
                return action.fromDict(d)

        raise ValueError("The dictionary does not correspond to any action")
