function GimberViewPort(displayId, divId) {

	// Setting of the image map
	var _mapSettings = {
		maxZoom: 21,
		minZoom: 0,
		crs: L.CRS.Simple
	}

	// Actual zoom level when zoom is supposed to be 0
	// This is used to obtain negative zoom level 
	var _zoomOffset = -3

	// Array containing the pixel values of the current image
	var _imageArray = null

	// Shape (width x eight x channels) of the current image
	var _imageShape = null

	// Tile layer object
	var _tiles = null

	// Map object
	var _imgMap = L.map(divId, _mapSettings).setView([0, 0], 0)
	
	// Overlay layer object
	var _overlays = L.layerGroup().addTo(_imgMap)



	// Load an image with the specified size in the display
	this.loadImage = function (image, shape) {
		var raw = window.atob(image)
		var rawLength = raw.length
		
		_imageShape = shape
		_imageArray = new Uint8Array(new ArrayBuffer(rawLength))
		for(i = 0; i < rawLength; i++)
			_imageArray[i] = raw.charCodeAt(i)
		
		if (_tiles !== null) {
			// Force the display to reload the tiles
			_tiles.redraw()
		}
		else {
			var tileUrl = '/tile/' + displayId + '/{z}/{x}/{y}'
			var tileSettings = {
				attribution: 'Gimber',
				zoomOffset: _zoomOffset,
				continuousWorld: true,
				maxNativeZoom: 8
			}

			_tiles = L.tileLayer(tileUrl, tileSettings).addTo(_imgMap);
		}
	}


	this.addPaths = function (paths) {
		$.each(paths, function(index, path){
			switch (path.ptype) {
				case "marker":
					var point = unproject(path.point)
					var marker = L.circleMarker(point, path.options)
					var popupText = "x=" + path.point[0].toFixed(2) + " y=" + path.point[1].toFixed(2)
					marker.bindPopup(popupText)
					_overlays.addLayer(marker)
					break

				case "line":
					var line = L.polyline(unprojectArray(path.points), path.options)
					_overlays.addLayer(line) 
					break
			}
		})
	}


	this.clearPaths = function() {
		_overlays.clearLayers()
	}

	
	// -------------- Pixel Information Control -----------------------

	var PixelInfoControl = L.Control.extend({
	    options: {
	        position: 'topright'
	    },

	    onAdd: function (imgMap) {
	        var container = L.DomUtil.create('div', 'pixel-info-control');
	        container.innerHTML = "<p>Pixel Info Control</p>"

	        function onMapMouseMove(e) {
		    	x = e.latlng.lng / Math.pow(2, _zoomOffset)
				y = -e.latlng.lat / Math.pow(2, _zoomOffset)
				container.innerHTML = "<p>x=" + x.toFixed(2) + " y=" + y.toFixed(2) + "</p>"

				if (_imageArray === null)
					return

				if (x < 0 || x > _imageShape[1] || y < 0 || x > _imageShape[0])
					return 

				if (_imageShape.length == 2) {
					var intensity = _imageArray[Math.floor(x) + Math.floor(y) * _imageShape[1]]
					var colorStr = "<p>Intensity: " + intensity
					colorStr += ' <span style="border: 1px;display: block;background: rgb('+ intensity +', '+ intensity +', '+ intensity +'); float: right;width: 15px;height: 15px;"> </span>'
					colorStr += "</p>"
				}
				else {
					var pixelIndex = 3 * Math.floor(x) + 3 * Math.floor(y) * _imageShape[1]
					var colorR = _imageArray[pixelIndex]
					var colorG = _imageArray[pixelIndex + 1]
					var colorB = _imageArray[pixelIndex + 2]
					var colorStr = '<p>Color: (' + colorR + ', ' + colorG + ', ' + colorB + ') '
					colorStr += '<span style="border: 1px;display: block;background: rgb('+ colorR +', '+ colorG +', '+ colorB +'); float: right;width: 15px;height: 15px;"> </span>'
					colorStr += '</p>'
				}

				container.innerHTML += colorStr
		    }

	        imgMap.on('mousemove', onMapMouseMove)
	        return container
	    }
	});

	_imgMap.addControl(new PixelInfoControl())	


	// ------------------- Auxiliary functions ---------------------------

	function unproject(point) {
		var scale = Math.pow(2, _zoomOffset)
		return [-point[1] * scale, point[0] * scale]
	}


	function unprojectArray(points) {
		$.each(points, function(i, point){
			points[i] = unproject(point)
		})
		return points
	}
}

// ========================================================================


function ActionsManager(gimberViewPort, actionsServerUrl) {

	var _gimberViewPort = gimberViewPort
	var _actionsUrl = actionsServerUrl
	var _last = 0
	var _delay = 500
	var _timerId = null


	function queryActions() {
		$.getJSON(_actionsUrl + _last, function(data) {
			// TODO: check data.result == "ok"

			_last = _last + data.actions.length

			$.each(data.actions, function(index, action){
				switch (action.atype) {
				case "loadimage":
					_gimberViewPort.loadImage(action.image, action.shape)
					break

				case "addpaths":
					_gimberViewPort.addPaths(action.paths)
					break
				
				case "clearpaths":
					_gimberViewPort.clearPaths()
					break

				case "empty":
					break
				}
			})
			_timerId = setTimeout(queryActions, _delay)
		});
	}


	this.start = function () {
		queryActions()
	}

	this.stop = function () {
		clearTimeout(_timerId)
		_timerId = null
	}

}