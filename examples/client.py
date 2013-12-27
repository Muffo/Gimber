""" Sample script that shows how to control a Gimber interactive server

Start the server before running this script:

    $ python -m gimber interactive

"""

from time import sleep
import cv2
import gimber


# Create a remote display manager object
# This will be used to get manage the displays available on the server
rdm = gimber.RemoteDisplayManager()

# Obtain a reference to the display called "display1"
# This create the display if not exist
display1 = rdm.get("display1")

# Load the image from file and add it to display1
image = cv2.imread("image.bmp", 0)
display1.loadImage(image)

# Remove all the overlays (points, lines) previously added
display1.clear()

# Open the display in the default browser
# The display can be accessed also from other devices at the URL:
# http://<ip-address>:8080/view/display1
display1.show()


# Infinite loop: add a grid to the display

gridSize = 30

while True:
    for y in range(10, 250, gridSize):
        for x in range(10, 250, gridSize):
            print "Add point (%d, %d)" % (x, y)

            # Add a point at the coordinates (x, y)
            # The display is automatically updated with the new marker on all the devices where it has been opened
            # The options specify additional parameters used while drawing the overlays on the image
            # Refer to the documentation of leaflet for the complete list: http://leafletjs.com/reference.html#path
            display1.addMarker([x, y], options={'radius': 4, 'weight': 6, 'color': 'white', 'fillColor': 'white'})

            # Add two lines to the display
            display1.addLine([[x, y], [x, y+gridSize]],  options={'color': 'red', 'weight': 3})
            display1.addLine([[x, y], [x+gridSize, y]],  options={'color': 'green', 'weight': 2})
            sleep(1)

    print "Clear display"
    display1.clear()
