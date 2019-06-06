window.onload = function () {

	//HTML elements

	var notif = document.getElementById('notif')//Text Area for Notifications
	var webcam_feed = document.getElementById("webcam_feed");//Video Element for Webcam Feed
	var set_selector = document.getElementById('set_selector');//Select Element to Choose Set
	var cardDisplay = document.getElementById('cardDisplay');//Image Element to Display Matched Card Image
	var cardName = document.getElementById('cardName');//Text Area to Display Matched Card Name
	var match_card_button = document.getElementById('match_card_button');//Button to Execute Matching

	//Global Variables
	var cam_working = false;//boolean to tell whether Webcam Feed is working

	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Access User's Webcam and feed to webcam_feed Element
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

	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Add All Stored Sets to Set Selector

	//Create set_list Request Object
	var set_list_request = new XMLHttpRequest();

	//Tell request to populat set_selector element after recieving reponse
	set_list_request.onload = function () {
		if (set_list_request.status >= 200 && set_list_request.status < 400) {
			respStr = set_list_request.response;

			//Split response array of setcodes
			respList = respStr.split('$');

			//Add each setcode to set_selector element
			for (var i = 0; i < respList.length; i++) {
				setcode = respList[i]
				let option = document.createElement("option");
				option.text = setcode;
				set_selector.add(option);
			}
		} else {
			console.log('set_list request completed incorrectly. Error', set_list_request.status);
		}
	};

	//Tell request what to do upon error
	set_list_request.onerror = function () {
		console.log("set_list didn't work at all");
	};

	//send request
	set_list_request.open('GET', '/set_list', true);
	set_list_request.send();

	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Matching System

	//Create Canvas Object for Temporary Image Processing
	var temp_canvas = document.createElement("CANVAS");
	var temp_context = temp_canvas.getContext('2d');

	//Create set_list Request Object
	var match_card_request = new XMLHttpRequest();

	//Tell request to display card after recieving reponse
	match_card_request.onload = function () {
		if (match_card_request.status >= 200 && match_card_request.status < 400) {
			respStr = match_card_request.response;

			//Split response into name and url
			respList = respStr.split('$');
			respName = respList[0];
			respMVID = respList[1];

			// Display card image from URL and name from name
			cardDisplay.src = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+respMVID+'&type=card';
			cardDisplay.onload = function () { // Display name only after image has loaded
				cardName.innerHTML = 'Card Name: ' + respName;
			}
		} else {
			console.log('Request completed incorrectly. Error', match_card_request.status);
		}
	};

	//Tell request what to do upon error
	match_card_request.onerror = function () {
		console.log("match_card didn't work at all");
	};

	//Tell match button to send request on click
	match_card_button.onclick = function () {
		if (cam_working) {

			//Remove info of previously matched card
			cardDisplay.src = 'resources/blankcard.png';
			cardDisplay.onload = function () {
				cardName.innerHTML = 'Card Name:';
			}

			//Capture image from webcam feed to temp canvas
			let vid_width = webcam_feed.videoWidth;
			let vid_height = webcam_feed.videoHeight;
			temp_canvas.width = vid_width;
			temp_canvas.height = vid_height;
			temp_context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);

			//Convert temp canvas image to PNG Data
			let capture = temp_canvas.toDataURL("image/png");

			//Create Form Data Object to send with Request
			let fd = new FormData();

			//Append PNG Data to Form
			fd.append('png', capture)

			//Append Setcode to Form
			fd.append('setcode', set_selector.options[set_selector.selectedIndex].value)

			//Send Request with Form
			match_card_request.open('POST', '/match_card', true);
			match_card_request.send(fd);
		} else {
			console.log('Camera Not Working, so cannot send image for match')
		}
	};
};
