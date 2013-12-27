""" Sample script that shows how to control a gimber interactive server

Start the server before running this script:

    $ python -m gimber interactive

"""

import cv2
import gimber


# Load the image
image = cv2.imread("chessboard.tif", 0)

# Look for the chessboard
patternSize = (16, 15)
found, corners = cv2.findChessboardCorners(image, patternSize,
                                           flags=(cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE))

# Refine the search of the corners
if found:
    term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
    cv2.cornerSubPix(image, corners, (5, 5), (-1, -1), term)


# Create a remote display manager object
# This will be used to get manage the displays available on the server
rdm = gimber.RemoteDisplayManager()

# Obtain a reference to the display called "chessboard"
# This create the display if not exist
display = rdm.get("chessboard")

# Load an image in the display
# The functions accepts the "image" variable of OpenCV
display.loadImage(image)

# Remove all the overlays (points, lines) previously added
display.clear()

# Draw the chessboard on the display
# The behavior is similar to the OpenCV function cv2.drawChessboardCorners
gimber.drawChessboardCorners(display, patternSize, corners, found)

# Open the display in the defaul browser
# The display can be accessed also from other devices at the URL:
# http://<ip-address>:8080/view/chessboard
display.show()