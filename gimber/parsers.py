#-------------------------------------------------------------------------------
# Name:        modulo1
# Purpose:
#
# Author:      GrandiAn
#
# Created:     11/09/2013
# Copyright:   (c) GrandiAn 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import argparse

# Parser for the server arguments

serverParser = argparse.ArgumentParser(add_help=False)

serverParser.add_argument("-H", "--host", default="0.0.0.0",
                    help="Server host to bind to")

serverParser.add_argument("-P", "--port", type=int, default=8080,
                    help="Server port to bind to")

serverParser.add_argument("-D", "--debug", action="store_true",
                    help="Run the server in debug mode")




# Parser for image formate arguments and other generic arguments

genericParser = argparse.ArgumentParser(add_help=False)

genericParser.add_argument("-s", "--tilesize", type=int, default=256,
                    help="Size of the tiles in pixels")

genericParser.add_argument("-f", "--format", choices=["png", "jpg", "bmp"], default="png",
                    help="Format of the images")

genericParser.add_argument("-c", "--compression", type=int, default=None,
                    help="Compression for .png [1-9] or quality of the images for .jpeg [1-100]")

genericParser.add_argument("-i", "--interp", choices=["none", "linear"], default="None",
                    help="Interpolation method used when scaling the images")


verbosityGroup = genericParser.add_mutually_exclusive_group()

verbosityGroup.add_argument("-v", "--verbose", action="store_true",
                    help="Print additional debug information")

verbosityGroup.add_argument("-q", "--quiet", action="store_true",
                    help="Suppress all the output to console")
