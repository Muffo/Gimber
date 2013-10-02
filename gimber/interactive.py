import os
import argparse
import json
import traceback

from gevent import monkey; monkey.patch_all()
import bottle

from parsers import serverParser, genericParser
from tiles import TileCreator, GenericTileServer
from display import LocalDisplay
from actions import ActionParser



class InteractiveTileServer(GenericTileServer):
    def __init__(self, tileSize, imageFormat, compression):
        super(InteractiveTileServer, self).__init__(tileSize, imageFormat, compression)
        self._displays = {}

    @classmethod
    def fromArgsConf(cls, conf):
        return cls(tileSize=conf.tilesize,
            imageFormat=conf.format, compression=conf.compression)

    @property
    def displays(self):
        return self._displays


    def home(self):
        # TODO: return a nice page with all the parameters
        return "The server is running!"


    def info(self):
        return {
            'displays': self.displays.keys()
        }


    def create(self):
        createDict = json.loads(bottle.request.body.read())
        if not createDict.has_key('displayId'):
            return self.exception('The displayId to create has not been specified')
        displayId = createDict['displayId']
        if self.displays.has_key(displayId):
            return self.exception("The display %s already exists" % (displayId))

        self.displays[displayId] = LocalDisplay()
        return {
            'result': 'ok',
            'message': "Display %s has been created" % (displayId)
        }


    def delete(self):
        deleteDict = json.loads(bottle.request.body.read())
        if not deleteDict.has_key('displayId'):
            return self.exception('The displayId to delete has not been specified')
        displayId = deleteDict['displayId']
        if not self.displays.has_key(displayId):
            return self.exception("The display %s does not exist" % (displayId))

        self.displays[displayId] = None
        self.displays.pop(displayId, None)
        return {
            'result': 'ok',
            'message': "Display %s has been deleted" % (displayId)
        }


    def do(self, displayId):
        if not self.displays.has_key(displayId):
            return self.exception("The display %s does not exist" % (displayId))

        display = self.displays[displayId]
        try:
            actionDict = json.loads(bottle.request.body.read())
            action = ActionParser.fromDict(actionDict)
            display.do(action)
        except Exception as e:
            return self.exception(e.message, details=traceback.format_exc())

        return {
            'result': 'ok',
            'message': "Action done on display %s" % (displayId)
        }


    def actions(self, displayId, last):
        if not self.displays.has_key(displayId):
            return self.exception("Display does not exist: %s" % (displayId))

        display = self.displays[displayId]
        try:
            actions = display.actionsFrom(last)
        except Exception as e:
            return self.exception(e.message, details=traceback.format_exc())

        return {
            'result': 'ok',
            'actions': [action.dict for action in actions]
        }


    def htmlError(self, message):
        errorTpl = os.path.join(self._root, 'resources/error')
        return bottle.template(errorTpl, message=message)


    def tile(self, displayId, x, y, z):
        if not self.displays.has_key(displayId):
            return self.htmlError("Display does not exist: %s" % (displayId))

        display = self.displays[displayId]

        if display.tileCreator is None:
            return self.emptyTile()

        tile = display.tileCreator.getTile(x, y, z)

        if tile is None:
            return self.emptyTile()

        bottle.response.content_type = self.imageEncoder.type
        return self.imageEncoder.encode(tile)


    def view(self, displayId):
        if not self.displays.has_key(displayId):
            return self.htmlError("Display does not exist: %s" % (displayId))

        viewTpl = os.path.join(self._root, 'resources/view')
        return bottle.template(viewTpl, displayId=displayId)


    def static(self, filename):
        root = os.path.join(self._root, 'resources')
        return bottle.static_file(filename, root=root)



def run(argv):
    parser = argparse.ArgumentParser(parents=[serverParser, genericParser])
    parser.description = """
    Launch an interactive web server that allows the user to interact with
    the images.

    Etc...
    """

    conf = parser.parse_args(argv)
    tileServer = InteractiveTileServer.fromArgsConf(conf)
    bottle.route('/', 'GET', tileServer.home)
    bottle.route('/info', 'GET', tileServer.info)
    bottle.route('/create', 'POST', tileServer.create)
    bottle.route('/delete', 'POST', tileServer.delete)
    bottle.route('/do/<displayId>', 'POST', tileServer.do)
    bottle.route('/actions/<displayId>/<last:int>', 'GET', tileServer.actions)
    bottle.route('/tile/<displayId>/<z:int>/<x:int>/<y:int>', 'GET', tileServer.tile)
    bottle.route('/view/<displayId>', 'GET', tileServer.view)
    bottle.route('/static/<filename:path>', 'GET', tileServer.static)

    # bottle.route('/tile/<z:int>/<x:int>/<y:int>/<filename:path>',
    #               'GET', tileServer.getTile)

    bottle.run(host=conf.host, port=conf.port,
                debug=conf.debug, quiet=conf.quiet, server='gevent')



if __name__ == "__main__":
    import sys
    run(sys.argv[1:])