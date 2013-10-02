""" Actions on the display

This module contains all the actions that can be done on a Display.
All the classes derive from the GernericAction and contain the atype field
(action type).

In addition, an ActionParser is provided that allow the system to
create the objects starting from a dictionary.
"""

import base64

import numpy as np

from paths import PathParser


class GenericAction(object):
    """ A generic action that can be done on a display

    Abstract class: do not instantiate
    """
    def __init__(self):
        pass


    @property
    def atype(self):
        """ Action type
        """
        return type(self).atype


    @property
    def dict(self):
        return {
            'atype': self.atype
        }


    @classmethod
    def checkDictAtype(cls, d):
        """ Check whether the atype of the dictionary matches the atype of the class
        """
        if not d.has_key('atype'):
            raise ValueError("The dictionary for the action does not contain the atype")

        if d['atype'] != cls.atype:
            raise ValueError("Action type (atype) does not match: %s != %s" %
                                                        (d['atype'], cls.atype))


    @classmethod
    def fromDict(cls, d):
        cls.checkDictAtype(d)
        # TODO: check that there are no extra parameters in the dictionary
        return cls()



class AddPaths(GenericAction):
    """ Add a list of paths to the display

    :params paths: list of Paths
    """
    def __init__(self, paths):
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
    """ Remove al the Paths from the display
    """
    atype = "clearpaths"


class EmptyAction(GenericAction):
    """ An action that does nothing

    This is typically used as a place holder for actions that have been removed from the display
    """
    atype = "empty"


class LoadImage(GenericAction):
    """ Load an image in the display
    """
    def __init__(self, image):
        self._image = image

    atype = "loadimage"


    @property
    def image(self):
        return self._image


    @classmethod
    def fromDict(cls, d):
        """ Create the object LoadImage from a dictionary

        The image is encoded in base64 so it is easier to transfer over an http connection
        """

        cls.checkDictAtype(d)
        if not d.has_key('image'):
            raise KeyError("LoadImage requires 'image': the content of the image (base64)")
        if not d.has_key('shape'):
            raise KeyError("LoadImage requires 'shape': [h, w] of the image")
        if len(d['shape']) != 2 and (len(d['shape']) == 3 and d['shape'][2] != 3):
            raise ValueError("Unvalid format for LoadImage' parameter 'shape': " + str(d['shape']))

        # TODO: add support for custom dtype
        imageBuffer = base64.decodestring(d['image'])
        image = np.frombuffer(imageBuffer, dtype=np.uint8)
        image.shape = d['shape']
        return LoadImage(image)


    @property
    def dict(self):
        return {
             'atype': self.atype,
             'image': base64.b64encode(self.image),
             'shape': self.image.shape
        }



class ActionParser(object):
    """ Utility class used to parse a dictionary that represents an action
    """
    actions = [AddPaths, ClearPaths, LoadImage, EmptyAction]

    @staticmethod
    def fromDict(d):
        for action in ActionParser.actions:
            if action.atype == d['atype']:
                return action.fromDict(d)

        raise ValueError("The dictionary does not correspond to any action")
