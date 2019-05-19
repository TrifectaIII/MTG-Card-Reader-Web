window.onload = function() {
	
	//Load Hidden Image from File
	var img = new Image();  
	img.src = 'test_web/cct_ima.png'
	img.onload = function(){
	}
	
	//Video Feed From Webcam
	var webcam_feed = document.getElementById("webcam_feed");
	
	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				webcam_feed.srcObject = stream;
			})
			.catch(function (err0r) {
				console.log("Something went wrong!");
			});
	}
	
	
	var width = 500;
	var height = 375;
	var canvas = document.getElementById('canvas');
	var context = canvas.getContext('2d');
	//var image = document.getElementById('image');
	
	var doFindFeatures = function() {
		tracking.Fast.THRESHOLD = 25;
		context.drawImage(webcam_feed, 0, 0, width, height);
		var imageData = context.getImageData(0, 0, width, height);
		var gray = tracking.Image.grayscale(imageData.data, width, height);
		var corners = tracking.Fast.findCorners(gray, width, height);
		console.log(corners.length);
		for (var i = 0; i < corners.length; i += 2) {
			context.fillStyle = '#ff00fa';
			context.fillRect(corners[i], corners[i + 1], 3, 3);
		}
	};
	//doFindFeatures();
	
	//Button to Process Frame of Webcam Video
	scan_button = document.getElementById('scan_button');
	scan_button.onclick = doFindFeatures;
}