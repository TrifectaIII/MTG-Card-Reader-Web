window.onload = function() {
	
	//Load Hidden Image from File
	var img = new Image();  
	img.src = 'test_web/cct_ima.png'
	img.onload = function(){
	}
	
	//Video Feed From Webcam
	var webcam_feed = document.getElementById("webcam_feed");
	
	var cam_working = false;
	
	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				webcam_feed.srcObject = stream;
				cam_working = true;
			})
			.catch(function (err0r) {
				console.log("Something went wrong!");
				cam_working = false;
			});
	}
	
	
	var vid_width;
	var vid_height;
	var canvas = document.getElementById('canvas');
	var context = canvas.getContext('2d');
	//var image = document.getElementById('image');
	
	
	//Button to Process Frame of Webcam Video
	scan_button = document.getElementById('scan_button');
	scan_button.onclick = function () {
		if (cam_working){
			vid_width = webcam_feed.videoWidth;
			vid_height = webcam_feed.videoHeight;
			canvas.width = vid_width;
			canvas.height = vid_height;
			var vid_features = findFeatures(35,webcam_feed,vid_width,vid_height);
			var vid_corners = vid_features.corners;
			context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);
			for (var i = 0; i < vid_corners.length; i += 2) {
					context.fillStyle = 'lime';
					context.fillRect(vid_corners[i], vid_corners[i + 1], 3, 3);
			}
		}
	};

	//delay = setInterval(scan_button.onclick,1000);
}