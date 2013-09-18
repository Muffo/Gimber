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
        return cls(paths)


class AddPaths(GenericAction):
    def __init__(self, paths):
        # super(AddPaths, self).__init__()
        self._paths = paths

    atype = "addpaths"

    @classmethod
    def fromDict(cls, d):
        cls.checkDictAtype(d)
        if d.has_key('paths'):
            raise KeyError("AddPaths requires 'paths': a list of paths")
        paths = [PathParser.fromDict(pd) for pd in d['paths']]
        return AddPaths(paths)

    @property
    def dict(self):
        return {
            'atype': self.atype,
            'paths': [e.dict for e in self._paths]
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
##    def __init__(self):
##        super(LoadImage, self).__init__()

    atype = "loadimage"



class ActionParser(object):

    actions = [AddPaths, ClearPaths, LoadImage, EmptyAction]

    @staticmethod
    def fromDict(d):
        for action in ActionParser.actions:
            if action.atype == d['atype']:
                return action.fromDict(d)

        raise ValueError("The dictionary does not correspond to any action")
