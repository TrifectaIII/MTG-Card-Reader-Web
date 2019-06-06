window.onload = function () {

	//Get HTML elements
	
	var notif = document.getElementById('notif')
	
	//Video Feed From Webcam
	var webcam_feed = document.getElementById("webcam_feed");

	var cam_working = false;

	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				webcam_feed.srcObject = stream;
				cam_working = true;
				notif.innerHTML = "Webcam Functional";
			})
			.catch(function (err0r) {
				console.log("Something went wrong!");
				cam_working = false;
				notif.innerHTML = "WebCam Error: Please ensure camera is connected and that this page has permission to use it.";
				notif.style.backgroundColor = 'lightcoral';
			});
	}

	//Add All Stored Sets to Set Selector
	var set_selector = document.getElementById('set_selector');
	var set_list_request = new XMLHttpRequest();
	set_list_request.onload = function () {
		if (set_list_request.status >= 200 && set_list_request.status < 400) {
			// Success!
			respStr  = set_list_request.response;
			//Split response into name and url
			respList  = respStr.split('$');
			for (var i = 0; i < respList.length; i++){
				setcode = respList[i]
				let option = document.createElement("option");
				option.text = setcode;
				set_selector.add(option);
			}
		} else {
			console.log('Request completed incorrectly. Error', set_list_request.status);
		}
	};
	set_list_request.onerror = function () {
		console.log("set_list didn't work at all");
	};

	set_list_request.open('GET','/set_list',true);
	set_list_request.send();



	//Setup For Matching
	var vid_width;
	var vid_height;
	// var canvas = document.getElementById('canvas');
	var temp_canvas  = document.createElement("CANVAS");
	var temp_context = temp_canvas.getContext('2d');

	//Card Display Image and Name Area
	cardDisplay = document.getElementById('cardDisplay');
	cardName    = document.getElementById('cardName');

	//Match Card Button and Requests
	var match_card_request = new XMLHttpRequest();
	match_card_request.onload = function () {
		if (match_card_request.status >= 200 && match_card_request.status < 400) {
			// Success!
			respStr  = match_card_request.response;
			//Split response into name and url
			respList = respStr.split('$');
			respName = 'Card Name: ' + respList[0];
			respURL  = respList[1];
			// Display card image from URL and name from name
			cardDisplay.src = respURL;
			cardDisplay.onload = function() { // Display name only after image has loaded
				cardName.innerHTML = respName;
			}
		} else {
			console.log('Request completed incorrectly. Error', match_card_request.status);
		}
	};
	match_card_request.onerror = function () {
		console.log("match_card didn't work at all");
	};

	var match_card_button = document.getElementById('match_card_button');
	match_card_button.onclick = function () {
		if (cam_working) {
			cardDisplay.src = 'resources/blankcard.png';
			cardDisplay.onload = function() { // Display name only after image has loaded
				cardName.innerHTML = 'Card Name:';
			}

			//Capture WebCam Image
			vid_width  = webcam_feed.videoWidth;
			vid_height = webcam_feed.videoHeight;
			temp_canvas.width  = vid_width;
			temp_canvas.height = vid_height;
			temp_context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);
			let capture = temp_canvas.toDataURL("image/png");

			//Append Image to Form
			let fd = new FormData();
			fd.append('png',capture)

			//Append Setcode to Form
			let set_selector = document.getElementById('set_selector');
			let setcode = set_selector.options[ set_selector.selectedIndex ].value
			fd.append('setcode',setcode)

			//Send Form with Request
			match_card_request.open('POST', '/match_card', true);
			match_card_request.send(fd);
		} else {
			console.log('Camera Not Working, so cannot send image for match')
		}
	};
};
