from gevent import monkey; monkey.patch_all()
import bottle
import argparse
from parsers import serverParser, genericParser
from tiles import TileCreator, GenericTileServer
import os


class InteractiveTileServer(GenericTileServer):
    def __init__(self, tileSize, imageFormat, compression):
        super(InteractiveTileServer, self).__init__(tileSize, imageFormat, compression)
        self.tileCreators = {}

    @classmethod
    def fromArgsConf(cls, conf):
        return cls(tileSize=conf.tilesize,
            imageFormat=conf.format, compression=conf.compression)

    @property
    def rootDir(self):
        return self._rootDir


    def hello(self):
        # TODO: return a nice page with all the parameters
        return "The server is running!"

    def echo(self, stringa):
        return str(stringa)


    '''
    def getTile(self, filename, x, y, z):

        if not self.tileCreators.has_key(filename):
            fileFullName = os.path.join(self.rootDir, filename)
            self.tileCreators[filename] = TileCreator.fromFile(fileFullName, self.tileSize)

        tile = self.tileCreators[filename].getTile(x, y, z)
        if tile is None:
            return bottle.static_file("1x1.png", root="resources/")

        bottle.response.content_type = self.imageEncoder.type
        return self.imageEncoder.encode(tile)

    '''


def run(argv):
    parser = argparse.ArgumentParser(parents=[serverParser, genericParser])
    parser.description = """
    Launch an interactive web server that allows the user to interact with
    the images.

    Etc...
    """

    print "Here we go"

    conf = parser.parse_args(argv)
    tileServer = InteractiveTileServer.fromArgsConf(conf)
    bottle.route('/hello', 'GET', tileServer.hello)
    bottle.route('/echo/<stringa>', 'GET', tileServer.echo)

    # bottle.route('/tile/<z:int>/<x:int>/<y:int>/<filename:path>',
    #               'GET', tileServer.getTile)

    bottle.run(host=conf.host, port=conf.port,
                debug=conf.debug, quiet=conf.quiet, server='gevent')




if __name__ == "__main__":
    import sys
    run(sys.argv[1:])