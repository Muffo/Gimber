<!DOCTYPE html>
<html>
<head>
	<title>{{displayId}} - Gimber interactive display</title>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.1/leaflet.css" />
	<link rel="stylesheet" href="/static/css/gimber.css" />
	<!--[if lte IE 8]>
	    <link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.1/leaflet.ie.css" />
	<![endif]-->

	<script src="http://cdn.leafletjs.com/leaflet-0.7/leaflet.js"></script>
	<script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
	<script src="/static/js/gimber.js"></script>

	<script type="text/javascript">
		
		$(function() {	
    		var displayId = "{{displayId}}"
    		var divId = "myDisplay"
    		var gimberView = new GimberViewPort(displayId, divId)
    		var actionsUrl = '/actions/' + displayId + '/'
    		var actions = new ActionsManager(gimberView, actionsUrl)
    		actions.start()
		});

	</script>

	</head>
	<body>
		 <div id="myDisplay" class="gimberDisplay"></div>		
	</body>
</html>
