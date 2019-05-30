window.onload = function () {

	//Video Feed From Webcam
	var webcam_feed = document.getElementById("webcam_feed");

	var cam_working = false;

	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				webcam_feed.srcObject = stream;
				cam_working = true;
				document.getElementById('notif').innerHTML = "Webcam Functional";
			})
			.catch(function (err0r) {
				console.log("Something went wrong!");
				cam_working = false;
				document.getElementById('notif').innerHTML = "WebCam Error: Please ensure camera is connected and that this page has permission to use it.";
				document.getElementById('notif').style.backgroundColor = 'lightcoral';
			});
	}



	//Setup
	var vid_width;
	var vid_height;
	// var canvas = document.getElementById('canvas');
	var temp_canvas = document.createElement("CANVAS");
	var temp_context = temp_canvas.getContext('2d');


	//Load Set Button and Requests
	var load_set_request = new XMLHttpRequest();
	load_set_request.onload = function () {
		if (load_set_request.status >= 200 && load_set_request.status < 400) {
			// Success!
			console.log(load_set_request.response);
		} else {
			console.log('Request completed incorrectly. Error', load_set_request.status)
		}
	};
	load_set_request.onerror = function () {
		console.log("load_set didn't work at all");
	};

	load_set_button = document.getElementById('load_set_button');
	load_set_button.onclick = function () {
		load_set_request.open('POST', '/load_set', true);
		load_set_request.send('setcode_placeholder');
	};

	//Match Card Button and Requests
	var match_card_request = new XMLHttpRequest();
	match_card_request.onload = function () {
		if (match_card_request.status >= 200 && match_card_request.status < 400) {
			// Success!
			console.log(match_card_request.response);
		} else {
			console.log('Request completed incorrectly. Error', match_card_request.status);
		}
	};
	match_card_request.onerror = function () {
		console.log("match_card didn't work at all");
	};

	match_card_button = document.getElementById('match_card_button');
	match_card_button.onclick = function () {
		if (cam_working) {
			vid_width = webcam_feed.videoWidth;
			vid_height = webcam_feed.videoHeight;
			temp_canvas.width = vid_width;
			temp_canvas.height = vid_height;
			temp_context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);
			var capture = temp_canvas.toDataURL("image/png");
			match_card_request.open('POST', '/match_card', true);
			match_card_request.send(capture);
		} else {
			console.log('Camera Not Working, so cannot send image for match')
		}
	};
};