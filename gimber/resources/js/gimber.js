$(function() {
	
    var map = L.map('map', {
		maxZoom: 8,
		minZoom: 0,
		crs: L.CRS.Simple
	}).setView([0, 0], 0);


	var tileUrl = '/tile/' + displayId + '/{z}/{x}/{y}'
	var zoomOffset = -3

	var tiles = L.tileLayer(tileUrl, {
		attribution: 'Gimber',
		zoomOffset: zoomOffset,
		continuousWorld: true
	}).addTo(map);


	var overlays = L.layerGroup().addTo(map)


	/*
	L.circle([5, -5], 10, {
		color: 'red',
		fillColor: '#f03',
		fillOpacity: 0.5
	}).addTo(map).bindPopup("I am a circle.");


	L.polygon([
		[-10, -10],
		[-10, 10],
		[10, 10],
		[10, -10]
	]).addTo(map).bindPopup("I am a polygon.");
	*/


	// -----------------------------------------------------------------

	var imageArray = null
	var imageShape = null

	function loadImage(image, shape) {
		var raw = window.atob(image)
		var rawLength = raw.length
		imageArray = new Uint8Array(new ArrayBuffer(rawLength))

		for(i = 0; i < rawLength; i++) {
			imageArray[i] = raw.charCodeAt(i)
		}
		imageShape = shape

		tiles.redraw()
	}


	function unproject(point) {
		return [-point[1] * Math.pow(2, zoomOffset), point[0] * Math.pow(2, zoomOffset)]
	}


	function addPaths(paths) {
		$.each(paths, function(index, path){
			switch (path.ptype) {
				case "marker":
					point = unproject(path.point)
					if (Object.keys(path.options).length != 0) {
						var marker = L.circleMarker(point, path.options)
					} else {
						var marker = L.circleMarker(point, 
							{'radius': 3, 'color': 'blue', 'fillColor': 'red'})
					}
					marker.bindPopup("x=" + path.point[0] + " y=" + path.point[1])
					overlays.addLayer(marker) 
					
					break

				case "line":
					if (Object.keys(path.options).length != 0) {
						var line = L.circleMarker(unproject(path.points[0]), path.options)
					} else {
						var line = L.circleMarker(unproject(path.points[0]), 
							{'radius': 3, 'color': 'blue', 'fillColor': 'red'})
					}
					overlays.addLayer(line) 
					break
			}
		})
	}


	function clearPaths() {
		overlays.clearLayers()
	}


	function dispatch(action) {
		switch (action.atype) {
			case "loadimage":
				loadImage(action.image, action.shape)
				break

			case "addpaths":
				addPaths(action.paths)
				break
			
			case "clearpaths":
				clearPaths()
				break

			case "empty":
				break
		}
	}

	// ------------------------------------------------------------------

	var PixelInfoControl = L.Control.extend({
	    options: {
	        position: 'topright'
	    },

	    onAdd: function (map) {
	        container = L.DomUtil.create('div', 'pixel-info-control');
	        container.innerHTML = "<p>Pixel Info Control</p>"

	        function onMapMouseMove(e) {
		    	x = e.latlng.lng / Math.pow(2, zoomOffset)
				y = -e.latlng.lat / Math.pow(2, zoomOffset)
				container.innerHTML = "<p>x=" + x.toFixed(3) + " y=" + y.toFixed(3) + "</p>"

				if (imageArray === null)
					return

				if (x < 0 || x > imageShape[1] || y < 0 || x > imageShape[0])
					return 

				if (imageShape.length == 2) {
					var intensity = imageArray[Math.floor(x) + Math.floor(y) * imageShape[1]]
					var colorStr = "<p>Intensity: " + intensity
					colorStr += ' <span style="border: 1px;display: block;background: rgb('+ intensity +', '+ intensity +', '+ intensity +'); float: right;width: 15px;height: 15px;"> </span>'
					colorStr += "</p>"
				}
				else {
					var colorR = imageArray[3 * Math.floor(x) + 3 * Math.floor(y) * imageShape[1]]
					var colorG = imageArray[3 * Math.floor(x) + 3 * Math.floor(y) * imageShape[1] + 1]
					var colorB = imageArray[3 * Math.floor(x) + 3 * Math.floor(y) * imageShape[1] + 2]
					var colorStr = "<p>Color: (" + colorR + ", " + colorG + ", " + colorB + ")"
					colorStr += ' <span style="border: 1px;display: block;background: rgb('+ colorR +', '+ colorG +', '+ colorB +'); float: right;width: 15px;height: 15px;"> </span>'
					colorStr += "</p>"
				}

				container.innerHTML += colorStr
		    }

	        map.on('mousemove', onMapMouseMove);

	        return container;
	    }
	});

	map.addControl(new PixelInfoControl());

	// -----------------------------------------------------------------

	var actionsUrl = '/actions/' + displayId + '/'
	var last = 0
	function queryActions() {
		$.getJSON(actionsUrl + last, function(data) {
			// TODO: check data.result == "ok"

			last = last + data.actions.length

			$.each(data.actions, function(index, action){
				dispatch(action)
			})
			setTimeout(queryActions, 500)
		});
	}

	queryActions()
});