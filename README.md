# Gimber

**Image tiles generator and interactive web viewer**


## Installation

At the moment there is no ready-to-use Python package.

First, you should make sure to fulfill all the libraries requirements. 
Then, download the source code here and add the gimber package in your PYTHONPATH. run gimber.py.

### Requirements:

#### Python

These Python libraries must be installed in order to run the server on you machine:

- [OpenCV](http://www.opencv.org): used for the image processing and compression
- [BottlePy](http://bottlepy.org): used for as web server
- [Gevent](http://www.gevent.org): enables multithreading in the server (much faster!!)

[BottlePy](http://bottlepy.org) consists of a single file and it can be manually copied in the PYTHONPATH.

Windows users can find the installer for OpenCV and Gevent [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/).
OSX and Linux users can refer to the official installation instructions.


#### Web Viewer

These Javascript libraries are used in the integrated web viewer. 
They will be downloaded from CDN, so you don't need to download them unless you plan to use the application offline:
- Leaflet.js
- Jquery



## Usage

The application can be used in 3 different modes:
1. Offline tile generator: generate all the tiles for a given image and save all the images in a folder
2. Static file server: start a web server that dynamically generates the tiles
3. Interactive display: show images and add overlays (point, line...) at runtime


### Offline tiles generator

Read the input image, generate all the tiles and finally save all the files in the output folder.
You can then copy all the images in your web server and use one of the many [JavaScript mapping libraries](http://gis.stackexchange.com/questions/8032/how-do-various-javascript-mapping-libraries-compare) already available to show the results.

You can see a [demo here](http://todo.add.demo.here).

#### Example

    python -m gimber tilesgen filename.jpg

#### Usage

	python -m gimber tilesgen [-h] [-s TILESIZE] [-f {png,jpg}] [-c COMPRESSION]
	                   		  [-i {none,linear}] [-v | -q] [-d DEST] [-z MINZOOM]
	                          [-Z MAXZOOM]
	                          inputImage

Positional arguments:

	inputImage            Image that will be used to create the tiles

Optional arguments:

	-h, --help            show this help message and exit
	-s TILESIZE, --tilesize TILESIZE
	                      Size of the tiles in pixels
	-f {png,jpg}, --format {png,jpg}
	                      Format of the images
	-c COMPRESSION, --compression COMPRESSION
	                      Compression for .png [1-9] or quality of the images
	                      for .jpeg [1-100]
	-i {none,linear}, --interp {none,linear}
	                      Interpolation method used when scaling the images
	-v, --verbose         Print additional debug information
	-q, --quiet           Suppress all the output to console
	-d DEST, --dest DEST  Folder that will contain the images
	-z MINZOOM, --minZoom MINZOOM
	                      Minimum zoom level used when rescaling the images
	-Z MAXZOOM, --maxZoom MAXZOOM
	                      Maximum zoom level used when rescaling the images

See also: [Zoom levels](#zoom-levels), [Image Formats](#image-formats)


### Static file server

Run a web server that generates the tiles dynamically for all the images contained in the specified folder.

#### Example:

    python -m gimber webserver

#### Usage:

	python -m gimber webserver [-h] [-H HOST] [-P PORT] [-D] [-s TILESIZE] [-f {png,jpg}]
                   			   [-c COMPRESSION] [-i {none,linear}] [-v | -q] [-d DIR]

Optional arguments:

	-h, --help            show this help message and exit
	-H HOST, --host HOST  Server host to bind to
	-P PORT, --port PORT  Server port to bind to
	-D, --debug           Run the server in debug mode
	-s TILESIZE, --tilesize TILESIZE
	                      Size of the tiles in pixels
	-f {png,jpg}, --format {png,jpg}
	                      Format of the images
	-c COMPRESSION, --compression COMPRESSION
	                      Compression for .png [1-9] or quality of the images
	                      for .jpeg [1-100]
	-i {none,linear}, --interp {none,linear}
	                      Interpolation method used when scaling the images
	-v, --verbose         Print additional debug information
	-q, --quiet           Suppress all the output to console
	-d DIR, --dir DIR     Directory that contains the image

See also: [Zoom levels](#zoom-levels), [Image Formats](#image-formats)


### Interactive display

Create an interactive display. 
Images can be dynamically loaded in the display using a public http API or the provided Python interface.
In addition, the display supports the 

The display can be viewed using any web browser, from both your PC and mobile device.

At the moment this mode is not intended to be used with an Internet connection, but only for local purposes.
For instance, it might be particularly useful in combination with OpenCV.

It is possible to interact with the display (loading an image, add points, lines, polygon...) using the public API.

#### Example:

    python -m gimber interactive

#### Usage:


See also: [Zoom levels](#zoom-levels), [Image Formats](#image-formats)

## Additional details


### Zoom levels


This will contains additional info about the zoom level:

- A table
- An example?


### Image formats

This will contains info about the file formats and parameters:

- Supported types
- Link to OpenCV ?
