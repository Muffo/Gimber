""" Auxiliary methods to replicate some OpenCV drawing function
"""


def drawChessboardCorners(display, patternSize, corners, patternWasFound):
    """ Renders the detected chessboard corners.

    The function draws individual chessboard corners detected either as red circles if the board was not found,
    or as colored corners connected with lines if the board was found.

    :param image: Destination display.
    :param patternSize: Number of inner corners per a chessboard row and column.
    :param corners: Array of detected corners, the output of findChessboardCorners.
    :param patternWasFound: Parameter indicating whether the complete board was found or not. The return value of findChessboardCorners() should be passed here.
    """
    if len(patternSize) != 2:
        raise ValueError("Pattern size format is not valid: " + str(patternSize))

    if len(corners.shape) != 3 or corners.shape[1] != 1 or corners.shape[2] != 2:
        raise ValueError("Corners format is not valid")

    colors = ['red', 'orange', 'yellow', 'lawngreen', 'lightblue', 'mediumblue', 'magenta']

    for r in range(patternSize[1]):
        color = colors[r % len(colors)] if patternWasFound else 'red'

        for c in range(patternSize[0]):
            idx = c + patternSize[0] * r
            point = corners[idx][0]
            display.addMarker(point, options={'radius': 3, 'color': color, 'fillColor': color})




def drawContours(display, contours, contourIdx, color, thickness, lineType, hierarchy, maxLevel, offset):
    """ Draws contours outlines or filled contours.

    :param display: Destination display.
    :param contours: All the input contours. Each contour is stored as a point vector.
    :param contourIdx: Parameter indicating a contour to draw. If it is negative, all the contours are drawn.
    :param color: Color of the contours.
    :param thickness: Thickness of lines the contours are drawn with. If it is negative (for example, thickness=CV_FILLED ), the contour interiors are drawn.
    :param lineType: Line connectivity. See line() for details.
    :param hierarchy: Optional information about hierarchy. It is only needed if you want to draw only some of the contours (see maxLevel ).
    :param maxLevel: Maximal level for drawn contours. If it is 0, only the specified contour is drawn. If it is 1, the function draws the contour(s) and all the nested contours. If it is 2, the function draws the contours, all the nested contours, all the nested-to-nested contours, and so on. This parameter is only taken into account when there is hierarchy available.
    :param offset: Optional contour shift parameter. Shift all the drawn contours by the specified  \texttt{offset}=(dx,dy) .
    :param contour: Pointer to the first contour.
    :param externalColor: Color of external contours.
    :param holeColor: Color of internal contours (holes).

    The function draws contour outlines in the image if \texttt{thickness} \ge 0 or fills the area bounded by the contours if \texttt{thickness}<0 .
    """
    pass
