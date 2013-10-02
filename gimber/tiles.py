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

import os

import bottle
import cv2
import numpy as np

"""
TODO:
    - Interpolation methods

"""

class TileCreator(object):

    def __init__(self, image, tileSize=256):
        self._image = image
        self._tileSize = float(tileSize)


    @classmethod
    def fromFile(cls, filePath, tileSize=256):
        """Load an image from file
        """
        image = cv2.imread(filePath)
        if image is None:
            raise IOError("Can't load image from: " + str(filePath))

        return cls(image, tileSize)


    @property
    def image(self):
        return self._image

##    @image.setter
##    def image(self, image):
##        # TODO: Here I could save an hash of the image to be used later...
##        self._image = image


    @property
    def height(self):
        """Height of the image"""
        return self._image.shape[0]

    @property
    def width(self):
        """Width of the image"""
        return self._image.shape[1]

    def scaleFactor(self, z=0):
        return pow(2, z)

    def regionSize(self, z=0):
        """Size on the image region at zoom leve = z"""
        return self._tileSize / self.scaleFactor(z)

    def nCols(self, z):
        """Number of column at zoom level = z"""
        return int(np.ceil(self.width / self.regionSize(z)))


    def nRows(self, z):
        """Number of column at zoom level = z"""
        return int(np.ceil(self.height / self.regionSize(z)))


    def getTile(self, x, y, z):
        """Return the selected tile or None if not exist"""

        if x < 0 or y < 0:
            return None

        regionSize = self.regionSize(z)
        rowStart = y * regionSize
        rowEnd = (y+1) * regionSize
        colStart = x * regionSize
        colEnd = (x+1) * regionSize

        if colStart >= self.width or rowStart >= self.height:
            return None

        if rowEnd <= 0 or colEnd <= 0:
            return None

        rowStart = max(rowStart, 0)
        rowEnd = min(rowEnd, self.height)
        colStart = max(colStart, 0)
        colEnd = min(colEnd, self.width)

        tile = self.image[rowStart:rowEnd, colStart:colEnd, :]

        scaleFactor = self.scaleFactor(z)
        if scaleFactor != 1:
            tile = cv2.resize(tile, (0, 0), fx=scaleFactor, fy=scaleFactor,
                                    interpolation=(cv2.INTER_NEAREST))

        return tile

##        (res, imageEncoded) = cv2.imencode(".png", imageRoi)
##        return imageEncoded.tostring()





class ImageEncoder(object):
    """
    For JPEG
    - quality from 0 to 100 (the higher is the better). Default value is 95.

    For PNG
    - compression level from 0 to 9. A higher value means a smaller size and
        longer compression time. Default value is 3.

    """
    def __init__(self, ext, params=None):

        ext = str(ext).lower()
        if ext[0] != ".":
            ext = "." + ext

        if ext not in [".png", ".jpeg", ".jpg", ".bmp"]:
            raise ValueError("Unsupported encoding: " + str(ext))

        if ext == ".png":
            if params is None:
                params = 3
            elif params < 0 or params > 9:
                raise ValueError("PNG compression level can be from 0 to 9: " + str(params))

        elif ext in [".jpg", ".jpeg"]:
            if params is None:
                params = 95
            elif params < 0 or params > 100:
                raise ValueError("JPEG quality can be from 0 to 100: " + str(params))

        if ext == ".bmp":
            if params is not None:
                raise ValueError("BMP does not accept any parameter: " + str(params))

        self._ext = ext
        self._params = params


    @property
    def ext(self):
        return self._ext

    @property
    def params(self):
        if self.ext == ".png":
            return (cv2.cv.CV_IMWRITE_PNG_COMPRESSION, self._params)

        elif self.ext in [".jpg", ".jpeg"]:
            return (cv2.cv.CV_IMWRITE_JPEG_QUALITY, self._params)

        if self.ext == ".bmp":
            return None


    @property
    def type(self):
        return "image/" + self.ext[1:]


    def encode(self, image):
        """Encode the image using the parameters specified in the constructor"""
        (result, encodedImage) = cv2.imencode(self.ext, image, self.params)

        if not result:
            raise RuntimeError("Image encoding has failed")

        return encodedImage.tostring()


#-------------------------------------------------------------------------------


class GenericTileServer(object):
    def __init__(self, tileSize, imageFormat, compression):
        self._tileSize = tileSize
        self._imageFormat = imageFormat
        self._compression = compression
        self._imageEncoder = ImageEncoder(imageFormat, compression)
        self._root = os.path.dirname(__file__)


    @property
    def tileSize(self):
        return self._tileSize

    @property
    def imageEncoder(self):
        return self._imageEncoder

    @property
    def imageFormat(self):
        return self.imageEncoder.ext

    @property
    def compression(self):
        return self.imageEncoder.params


    def exception(self, message, details=None):
        errorDict = {
            'result': 'error',
            'message': message,
        }

        if details is not None:
            errorDict['details'] = details

        return errorDict


    def emptyTile(self):
        resourcesPath = os.path.join(self._root, 'resources')
        return bottle.static_file("img/1x1.png", root=resourcesPath)




