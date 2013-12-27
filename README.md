# Gimber

**Interactive image web viewer**

## Key Features
 
- **OpenCV native support**: the application has been written with OpenCV and Python in mind, hence it comes with native support for the datastructures of the library. The porting of your pre-existing application to the new visualization library should be straightforward

- **Multiple displays**: multiple displays can be shown simultaneously on different devices. Both PCs and mobile devices are supported. That means you can write the code on an interactive shell of your PC and display the images on your tablet

- **Inteactive**: the user can load images at any time on the display or add overlays (i.e. lines and points). The changes are applied in real time on all the active displays

- **Sub-pixel resolution**: the image and the overlays are kept separated. At high level of zoom the pixels of the image get visible, while the overlays are always drawn with sub-pixel accuracy

- **Public HTTP API**: the display can be controlled with the public HTTP API from virtually any programming language, although a Python wrapper is given out of the box

- **Platform independent server**: the server is written in Python and can run on all the major platforms


## Installation

At the moment there is no ready-to-use Python package.

First, you should make sure to fulfill all the libraries requirements. 
Then, download the source code here and add the gimber package in your PYTHONPATH. run gimber.py.

### Requirements:

#### Python

These Python libraries must be installed in order to run the server on you machine:

- [OpenCV](http://www.opencv.org): image processing and compression
- [BottlePy](http://bottlepy.org): web server
- [Gevent](http://www.gevent.org): enables multithreading in the server (much faster!!)
- [Urllib3](https://github.com/shazow/urllib3) + [Requests](http://docs.python-requests.org): more efficient HTTP requests with keep alive

[BottlePy](http://bottlepy.org) consists of a single file and it can be manually copied in the PYTHONPATH.

Windows users can find the installer for OpenCV and Gevent [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/).
OSX and Linux users can refer to the official installation instructions.


#### Web Viewer

The following Javascript libraries are used in the integrated web viewer:
- [Leaflet.js](http://leafletjs.com)
- [Jquery](http://jquery.com)

They will be automatically obtained from CDN, so you don't need to download them unless you plan to use the application offline.



## Interactive display

The Gimber server must be started in order to create the interactive display.

Images can be dynamically loaded in the display using a public http API or the provided Python interface.
The API can also be used to interact with the display: add points, lines, polygon...
The documentation of the API is not ready yet. 
Please refer to the python examples contained in the repository.

The display can be viewed from any web browser, from both your PC and mobile device.

At the moment this mode is not intended to be used with an Internet connection, but only for local purposes.
For instance, it might be particularly useful when debugging an application written in Python+OpenCV.



#### Example:

    python -m gimber interactive

#### Usage:

python -m gimber interactive [-h] [-H HOST] [-P PORT] [-D] [-s TILESIZE] [-f {png,jpg}]
                   			 [-c COMPRESSION] [-i {none,linear}] [-v | -q]


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

TODO: complete this part


## Other features

The following features are also available:
1. Offline tile generator: generate all the tiles for a given image and save all the images in a folder
2. Static file server: start a web server that dynamically generates the tiles

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

The tiles of all the images contained in the folder where the server has been started will be available at the following address:

	http://localhost:8080/tile/<z:int>/<x:int>/<y:int>/<filename:path>

If you are using leaflet.js to display the tiles you can use a tileUrl like the follow:

```javascript
	var tileUrl = "http://localhost:8080/tile/{z}/{x}/{y}/path/to/image.png"  
```

You can change the root folder using the command line argument --dir.

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
