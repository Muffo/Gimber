from gevent import monkey; monkey.patch_all()
import bottle
import argparse
from parsers import serverParser, genericParser
from tiles import TileCreator, GenericTileServer
import os


class StaticTileServer(GenericTileServer):
    def __init__(self, rootDir, tileSize, imageFormat, compression):
        super(StaticTileServer, self).__init__(tileSize, imageFormat, compression)

        self._rootDir = rootDir
        self.tileCreators = {}


    @staticmethod
    def fromArgsConf(conf):
        return StaticTileServer(rootDir=conf.dir, tileSize=conf.tilesize,
            imageFormat=conf.format, compression=conf.compression)


    def hello(self):
        # TODO: return a nice page with all the parameters
        return "The interactive server is running!"


    def getTile(self, filename, x, y, z):
        if not self.tileCreators.has_key(filename):
            fileFullName = os.path.join(self.rootDir, filename)
            self.tileCreators[filename] = TileCreator.fromFile(fileFullName, self.tileSize)

        tile = self.tileCreators[filename].getTile(x, y, z)
        if tile is None:
            return bottle.static_file("1x1.png", root="resources/")

        bottle.response.content_type = self.imageEncoder.type
        return self.imageEncoder.encode(tile)



def run(argv):
    parser = argparse.ArgumentParser(parents=[serverParser, genericParser])
    parser.description = """
    Launch a web server that generate the tiles on demand in the current folder,
    unless a different root is specified in the parameters.

    The format of the images...

    Other details here.
    """

    parser.add_argument("-d", "--dir", default=".",
                        help="Directory that contains the image")

    conf = parser.parse_args(argv)
    print conf


    tileServer = StaticTileServer.fromArgsConf(conf)
    bottle.route('/hello', 'GET', tileServer.hello)
    bottle.route('/tile/<z:int>/<x:int>/<y:int>/<filename:path>', 'GET', tileServer.getTile)

    bottle.run(host=conf.host, port=conf.port,
                debug=conf.debug, quiet=conf.quiet, server='gevent')






if __name__ == "__main__":
    import sys
    run(sys.argv[1:])