""" Display

The display is the object used to show the images and perform actions on it like adding markers, lines, etc ...

The module contains the definition of different types of display:
- AbstractDisplay: abstract class defining the properties shared by all the displays
- LocalDisplay: a display that is typically created by the interactive server
- RemoteDisplay: a proxy that is used to interact with a LocalDisplay on a remote machine

In addition the RemoteDisplayManager is used to create/delete the displays on a remote machine

"""

import requests
from urlparse import urljoin
import json
import webbrowser
from requests.exceptions import ConnectionError

from tiles import *
from actions import *
from paths import *

class AbstractDisplay(object):
    """ AbstractDisplay that provides basic features for all the display

    Do not directly use this class
    """
    def __init__(self):
        raise RuntimeError("Cannot create an instance of AbstractDisplay")


    def actionsFrom(self, last):
        """ Actions executed on the display from "last"

        The client should keep track of the "last" (progressive integer) action that has asked
        Abstract method: implement in the concrete classes
        """
        raise NotImplementedError()


    def do(self, action):
        """Execute an action on the display

        Abstract method: implement in the concrete classes
        """
        raise NotImplementedError()


    def addMarker(self, point, options={}):
        """ Add a marker to the display

        :param point: the coordinates of the Marker
        :param options: a dictionary containing the options of the Marker
        """
        marker = Marker(point, options)
        action = AddPaths([marker])
        self.do(action)


    def addLine(self, points, options={}):
        """ Add a marker to the display

        :param point: the coordinates of two points of the Line
        :param options: a dictionary containing the options of the Line
        """
        line = Line(points, options)
        action = AddPaths([line])
        self.do(action)


    def clear(self):
        """ Clear the display removing all the Paths (Markers, Line, ...)
        """
        action = ClearPaths()
        self.do(action)


    def loadImage(self, image):
        """ Load the image in the display
        """
        action = LoadImage(image)
        self.do(action)

#-------------------------------------------------------------------------------


class LocalDisplay(AbstractDisplay):
    """ A display that is created and used in a local context
    """
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
    """ Exception raised when the server encountered an error
    """
    def __init__(self, message, details=""):
        self.message = message
        self.details = details


    @classmethod
    def fromDict(cls, d):
        """ Create the object starting from a dictionary

        The dictionary must have the key 'message' and an optional key 'details'
        """
        if d.has_key('details'):
            return cls(d['message'], d['details'])
        else:
            return cls(d['message'])


    def __str__(self):
         return self.message



class RemoteDisplay(AbstractDisplay):
    """ A proxy used to communicate with a remote display that has been instantiated on an interactive server

    :param name: the name used to identify the display
    :param url: the url of the interactive server that contains the display
    """
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
        return urljoin(self.url, "do/" + self.name)


    @property
    def actionsUrl(self):
        return urljoin(self.url, "actions/" + self.name)


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


    def show(self):
        """ Show the display on the default web browser
        """
        webbrowser.open(urljoin(self.url,  "view/" + self.name))



class RemoteDisplayManager(object):
    """ A manager used to create and delete the displays on an interactive server
    """
    def __init__(self, url="http://localhost:8080"):
        self._url = url
        self._displays = {}
        self._session = requests.Session()

        try:
            self.session.get(self.infoUrl)
        except ConnectionError:
            raise ConnectionError("Failed to connect to interactive server at url: " + url)


    @property
    def url(self):
        return self._url


    @property
    def session(self):
        """ Session used to increase the speed of the requests
        """
        return self._session


    @property
    def createUrl(self):
        """ The Url of the API used to create a new display
        """
        return urljoin(self.url, "create")


    @property
    def deleteUrl(self):
        """ The Url of the API used to delete a display
        """
        return urljoin(self.url, "delete")


    @property
    def infoUrl(self):
        """ The Url of the API used to obtain the info of the remote server
        """
        return urljoin(self.url, "info")


    def create(self, name):
        """ Create the display in the interactive server

        :params name: the name used to identify the display
        :returns: a RemoteDisplay object that can be used to interact with the display
        """
        reqJson = json.dumps({"displayId": name})
        response = self.session.post(self.createUrl, data=reqJson).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)
        return RemoteDisplay(name, self.url)


    def delete(self, name):
        """ Delete the display in the interactive server

        :params name: the name of the display to delete
        """
        reqJson = json.dumps({"displayId": name})
        response = self.session.post(self.deleteUrl, data=reqJson).json()
        if response['result'] != "ok":
            raise ServerSideError.fromDict(response)




