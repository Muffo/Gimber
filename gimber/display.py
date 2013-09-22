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

import requests
from urlparse import urljoin
import json

from tiles import *
from actions import *
from paths import *

class AbstractDisplay(object):
    def __init__(self):
        raise RuntimeError("Cannot create an instance of AbstractDisplay")

    def actionsFrom(self, last):
        raise NotImplementedError()


    def do(self, action):
        raise NotImplementedError()


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

#-------------------------------------------------------------------------------


class LocalDisplay(AbstractDisplay):
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


#-------------------------------------------------------------------------------


class ServerSideError(Exception):
    def __init__(self, message, details=""):
         self.message = message
         self.details = details


    @classmethod
    def fromDict(cls, d):
        if d.has_key('details'):
            return cls(d['message'], d['details'])
        else:
            return cls(d['message'])


    def __str__(self):
         return self.message



class RemoteDisplay(AbstractDisplay):
    def __init__(self, name, url):
        self._name = name
        self._url = url
        self._session = requests.Session()


    @property
    def name(self):
        return self._name


    @property
    def url(self):
        return self._url


    @property
    def doUrl(self):
        return urljoin(self._url, "do/" + self.name)


    @property
    def actionsUrl(self):
        return urljoin(self._url, "actions/" + self.name)


    def actionsFrom(self, last):
        actionsUrl = self.actionsUrl + "/" + str(last)
        response = self._session.get(actionsUrl).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)
        return [ActionParser.fromDict(d) for d in response['actions']]


    def do(self, action):
        actionJson = json.dumps(action.dict)
        response = self._session.post(self.doUrl, data=actionJson).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)



class RemoteDisplayManager(object):
    def __init__(self, url):
        self._url = url
        self._displays = {}
        self._session = requests.Session()


    @property
    def url(self):
        return self._url


    @property
    def createUrl(self):
        return urljoin(self._url, "create")


    @property
    def deleteUrl(self):
        return urljoin(self._url, "delete")


    def create(self, name):
        reqJson = json.dumps({"displayId": name})
        response = self._session.post(self.createUrl, data=reqJson).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)
        return RemoteDisplay(name, self.url)


    def delete(self, name):
        reqJson = json.dumps({"displayId": name})
        response = self._session.post(self.deleteUrl, data=reqJson).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)




