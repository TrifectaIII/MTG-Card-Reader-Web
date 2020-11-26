// JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

// Handle video feed using webrtc, allow users to switch camera with selector
//////////////////////////////////////////////////////////////////////////////

// Populate Video Selector
var gotDevices = function (deviceInfos) {

	//Remove all pre-exisiting options
	for(let i = cam_select.options.length - 1 ; i >= 0 ; i--){
	    cam_select.remove(i);
	}

	//add all video devices to selector
	for (let i = 0; i < deviceInfos.length; ++i) {
		let deviceInfo = deviceInfos[i];
		if (deviceInfo.kind === 'videoinput') {
			let existed = false;
			for (let j = 0; j < cam_select.options.length; j++) {
				if (cam_select.options[j].value == deviceInfo.deviceId) {
					cam_select.options[j].text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
					existed = true;
				}
			}
			if (!existed) {
				let option = document.createElement('option');
				option.value = deviceInfo.deviceId;
				option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
				cam_select.appendChild(option);
			}
		}
	}
};

//What to do when camera errors
var errorDevices = function (error) {
	console.log('navigator.MediaDevices.getUserMedia error: ', error);
	cam_working = false;
	notify("Video Error: Could not connect to video device. Please ensure camera is connected and that this page has\
	 permission to use it, then reload the video feed. Or, select another video device.");
	identify_card_button.disabled = true;
}

navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(errorDevices);

//What to do when camera works
var gotStream = function (stream) {
	window.stream = stream; // make stream available to console
	webcam_feed.srcObject = stream;

	cam_working = true;

	//Enable identify button once set is selected and camera is working
	if (set_selected) {
		identify_card_button.disabled = false;
	};

	// Refresh button list in case labels have become available
	return navigator.mediaDevices.enumerateDevices();
}

var start = function () {
	// stop all running tracks
	if (window.stream) {
		window.stream.getTracks().forEach(track => {
			track.stop();
		});
	}
	identify_card_button.disabled = true;

	let videoSource = cam_select.value;
	let constraints = {
		video: { deviceId: videoSource ? { exact: videoSource } : undefined }
	}

	navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(gotDevices).catch(errorDevices);
}

cam_select.addEventListener('change', start);

reload_cam_button.addEventListener('click', start);

start();