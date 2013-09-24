<!DOCTYPE html>
<html>
<head>
	<title>{{displayId}} - Gimber interactive display</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.css" />
	<link rel="stylesheet" href="static/css/gimber.css" />
	<!--[if lte IE 8]>
	    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.ie.css" />
	<![endif]-->

	<script src="http://cdn.leafletjs.com/leaflet-0.6.4/leaflet.js"></script>
	<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
	<script src="static/js/gimber.js"></script>

	<script type="text/javascript">
		var displayId = {{displayId}}
	</script>

	</head>
	<body>
		 <div id="map"></div>		
	</body>
</html>
