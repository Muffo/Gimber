import argparse
from parsers import genericParser
import os

from tiles import TileCreator, ImageEncoder

def run(argv):
    parser = argparse.ArgumentParser(parents=[genericParser])
    parser.description = """
    Creates and saves on disk all the tiles for the specified image
    """

    parser.add_argument("inputImage",
                        help="Image that will be used to create the tiles")

    parser.add_argument("-d", "--dest", default=None,
                        help="Folder that will contain the images")

    parser.add_argument("-z", "--minZoom", type=int, default=-2,
                        help="Minimum zoom level used when rescaling the images")

    parser.add_argument("-Z", "--maxZoom", type=int, default=2,
                        help="Maximum zoom level used when rescaling the images")

    conf = parser.parse_args(argv)



    # If dest is not specified, creates a folder with the same name of the image
    if conf.dest is None:
        conf.dest = os.path.join(os.path.dirname(conf.inputImage),
                                 os.path.basename(conf.inputImage).replace(".", "_"))


    if conf.verbose:
        # TODO: improve with the logger and more readable output...
        print conf


    tileCreator = TileCreator.fromFile(conf.inputImage, conf.tilesize)
    imageEncoder = ImageEncoder(conf.format, conf.compression)


    for z in range(conf.minZoom, conf.maxZoom):
        for x in range(tileCreator.nCols(z)):
            destFolder = os.path.join(conf.dest, str(z-conf.minZoom), str(x))
            if not os.path.exists(destFolder):
                    os.makedirs(destFolder)

            for y in range(tileCreator.nRows(z)):
                tile = tileCreator.getTile(x, y, z)
                if tile is None:
                    raise RuntimeError("Tile is None for x=%d y=%d z=%d" % (x, y, z))

                encodedTile = imageEncoder.encode(tile)
                destFile = os.path.join(destFolder, str(y) + "." + conf.format)

                with open(destFile, 'wb') as f:
                    f.write(encodedTile)


if __name__ == "__main__":
    import sys
    run(sys.argv[1:])






