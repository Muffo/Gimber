$(function() {
	
    var map = L.map('map', {
		maxZoom: 7,
		minZoom: 0,
		crs: L.CRS.Simple
	}).setView([0, 0], 0);

	// ? Sets a map view that contains the given geographical bounds with the maximum zoom level possible.
	// map.fitBounds([
    //    L.CRS.Simple.pointToLatLng(new L.Point(0, 0), 13),
    //    L.CRS.Simple.pointToLatLng(new L.Point(500, 300), 13)
    // ]);

	var tileUrl = '/tile/' + displayId + '/{z}/{x}/{y}'
	var tiles = L.tileLayer(tileUrl, {
		attribution: 'Gimber',
		zoomOffset: -3,
		continuousWorld: true
	}).addTo(map);


	var overlays = L.layerGroup().addTo(map)


	/*
	var m = {
	  x: 0, 
	  y: 0
	}
	var marker = L.marker(map.unproject([m.x, m.y], map.getMaxZoom())).addTo(map)
		.bindPopup("<b>This is the center</b><br />");


	L.marker([-255, 255]).addTo(map)
		.bindPopup("<b>This is somewhere else</b><br />");


	L.circle([5, -5], 10, {
		color: 'red',
		fillColor: '#f03',
		fillOpacity: 0.5
	}).addTo(map).bindPopup("I am a circle.");

	L.circleMarker([5, 5], {
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


	var popup = L.popup();
	function onMapClick(e) {
		x = e.latlng.lng
		y = -e.latlng.lat

		popup
			.setLatLng(e.latlng)
			.setContent("x=" + x + " y=" + y)
			.openOn(map);
	}
	map.on('click', onMapClick);


	function onMapMouseMove(e) {
		x = e.latlng.lng
		y = -e.latlng.lat
		console.log("x=" + x + " y=" + y)
	}
	// map.on('mousemove', onMapMouseMove);


	// -----------------------------------------------------------------

	function loadImage() {
		tiles.redraw()
	}


	function unproject(point) {
		return [-point[1], point[0]]
	}

	function addPaths(paths) {
		$.each(paths, function(index, path){
			switch (path.ptype) {
				case "marker":
					if (Object.keys(path.options).length != 0) {
						var marker = L.circleMarker(unproject(path.point), path.options)
					} else {
						var marker = L.circleMarker(unproject(path.point), 
							{'radius': 2, 'color': 'blue', 'fillColor': 'red'})
					}
					overlays.addLayer(marker) 
					//marker.addTo(map)
					break

				case "line":
					if (Object.keys(path.options).length != 0) {
						var line = L.circleMarker(unproject(path.points[0]), path.options)
					} else {
						var line = L.circleMarker(unproject(path.points[0]), 
							{'radius': 2, 'color': 'blue', 'fillColor': 'red'})
					}
					overlays.addLayer(line) 
					// line.addTo(map)
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
				loadImage()
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