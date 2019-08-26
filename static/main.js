// Primary JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web


// VIDEO
//////////////////////////////////////////////////////////////////////////////

// Populate Video Selector
var gotDevices = function (deviceInfos) {

	// Remove all pre-exisiting options
	// for(let i = cam_select.options.length - 1 ; i >= 0 ; i--){
	//     cam_select.remove(i);
	// };

	//add all video devices to selector
	for (let i = 0; i < deviceInfos.length; ++i) {
		let deviceInfo = deviceInfos[i];
		if (deviceInfo.kind === 'videoinput') {
			let existed = false;
			for (let j = 0; j < cam_select.options.length; j++) {
				if (cam_select.options[j].value == deviceInfo.deviceId) {
					cam_select.options[j].text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
					existed = true;
				};
			};
			if (!existed) {
				let option = document.createElement('option');
				option.value = deviceInfo.deviceId;
				option.text = deviceInfo.label || `camera ${videoSelect.length + 1}`;
				cam_select.appendChild(option);
			};
		} else {
			// do nothing if device is not videoinput
		};
	};
};

//What to do when camera errors
var errorDevices = function (error) {
	console.log('navigator.MediaDevices.getUserMedia error: ', error.message, error.name);
	cam_working = false;
	notify("Video Error: Could not connect to video device. Please ensure camera is connected and that this page has\
	 permission to use it, then reload the video feed. Or, select another video device.");
	identify_card_button.disabled = true;
};

navigator.mediaDevices.enumerateDevices().then(gotDevices).catch(errorDevices);

//What to do when camera works
var gotStream = function (stream) {
	window.stream = stream; // make stream available to console
	webcam_feed.srcObject = stream;

	cam_working = true;
	// notif_text.innerHTML = "Webcam Functional";

	//Enable identify button once set is selected and camera is working
	if (set_selected) {
		identify_card_button.disabled = false;
	};

	// Refresh button list in case labels have become available
	return navigator.mediaDevices.enumerateDevices();
};

var start = function () {
	// stop all running tracks
	if (window.stream) {
		window.stream.getTracks().forEach(track => {
			track.stop();
		});
	};

	// notif_text.innerHTML = "Loading Webcam...";
	identify_card_button.disabled = true;

	let videoSource = cam_select.value;
	let constraints = {
		video: { deviceId: videoSource ? { exact: videoSource } : undefined }
	};

	navigator.mediaDevices.getUserMedia(constraints).then(gotStream).then(gotDevices).catch(errorDevices);
};

cam_select.onchange = start;

reload_cam_button.addEventListener('click', start);

start();

// POPULATE SET LIST
//////////////////////////////////////////////////////////////////////////////

//Turn set_selector into Choices element
var set_selector_choice = new Choices(set_selector, {
	//Options for Choices element
	addItems: true,
	removeItems: false,
	renderChoiceLimit: -1,
	searchResultLimit: 5,
	searchPlaceholderValue: "Search by Set Name or Code:",
	itemSelectText: '',
});

//Enable identify button once set is selected and camera is working
set_selector.addEventListener('choice', function () {
	if (sets_load) {
		set_selected = true;
		if (cam_working) {
			identify_card_button.disabled = false;
		};
	};
});

//Create set_list Request Object
var set_list_request = new XMLHttpRequest();

//Tell request to populat set_selector element after recieving reponse
set_list_request.onload = function () {
	if (set_list_request.status >= 200 && set_list_request.status < 400) {

		//Get full response as JSON
		let respJSON = JSON.parse(set_list_request.response);

		//Init List of Choice Objects
		let choiceList = [];

		//for each set in JSON, add set to choiceList
		for (let setcode in respJSON) {
			let setname = respJSON[setcode];
			choiceList.push({
				value: setcode,
				label: setname + ' (' + setcode + ')',
				selected: false,
				disabled: false,
			});
		};

		//Add all set Choice objects to Choices element
		set_selector_choice.setChoices(choiceList, 'value', 'label', true);
		sets_load = true;

	} else {
		console.log('set_list request completed incorrectly. Error', set_list_request.status);
	};
};

//Tell request what to do upon error
set_list_request.onerror = function () {
	console.log("set_list request failed");
	notify('Server Error: set_list request failed. Please reload page and try again.');
};

//send request targeting sets.json file
set_list_request.open('GET', '/static/sets.json', true);
set_list_request.send();

// MATCHING SYSTEM
//////////////////////////////////////////////////////////////////////////////

//Create Canvas Object for Temporary Image Processing
var temp_canvas = document.createElement("CANVAS");
var temp_context = temp_canvas.getContext('2d');

//Create set_list Request Object
var identify_card_request = new XMLHttpRequest();

//Tell request to display card after recieving reponse
identify_card_request.onload = function () {
	if (identify_card_request.status >= 200 && identify_card_request.status < 400) {

		//Calculate Response Time and log to console
		console.log('/identify_card Response Time (s):', (Date.now() - identify_start) / 1000);

		//Get full response as JSON
		let respJSON = JSON.parse(identify_card_request.response);

		//Access response for name and url
		let identifiedName = respJSON.name;
		let identifiedMVID = respJSON.mvid;
		let identifiedPurchaseUrls = respJSON.purchaseUrls;

		console.log(identifiedPurchaseUrls);

		if (identifiedName.length == 0) {
			// If no identify is made, display error
			card_image.onload = function () {
				card_name.innerHTML = 'IDENTIFY ERROR';
				notify('Identification Error: Unable to identify card. Please ensure card is against a neutral background.');
			};
			card_image.src = '/static/errorcard.png';
		} else {
			// Display card image from URL and name from name
			card_image.onload = function () {
				// Display name only after image has loaded
				card_name.innerHTML = identifiedName;
				//Enable adding Buttons also after image has loaded
				enableButtons(addremovebuttons);
			};
			card_image.src = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=' + identifiedMVID + '&type=card';
		};
	} else {
		console.log('Request completed incorrectly. Error', identify_card_request.status);
	};
};

//Tell request what to do upon error
identify_card_request.onerror = function () {
	console.log("identify_card didn't work at all");

	//display error image
	card_image.onload = function () {
		card_name.innerHTML = 'SERVER ERROR';
		notify('Server Error: identify_card request failed. Please reload page and try again.')
	};
	card_image.src = '/static/errorcard.png';

};

//Tell identify button to send request on click
identify_card_button.addEventListener('click', function () {
	if (cam_working) {

		//start response timer
		identify_start = Date.now();

		//Remove previous card and display loading
		card_image.onload = function () {
			card_name.innerHTML = 'Loading...';
			card_name.style.backgroundColor = '';
			//Disable all adding buttons until new card identifyed
			disableButtons(addremovebuttons);
		};
		card_image.src = '/static/loadingcard.gif';


		//Capture image from webcam feed to temp canvas
		let vid_width = webcam_feed.videoWidth;
		let vid_height = webcam_feed.videoHeight;
		temp_canvas.width = vid_width;
		temp_canvas.height = vid_height;
		temp_context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);

		//Convert temp canvas image to PNG/JPG Data
		let capture = temp_canvas.toDataURL("image/jpeg", 0.1); //Send as JPG, numeric argument is quality (higher is better quality)
		//let capture = temp_canvas.toDataURL("image/png"); //Send as PNG

		//Create Form Data Object to send with Request
		let fd = new FormData();

		//Append PNG Data to Form
		fd.append('image', capture);

		//Append Setcode to Form
		fd.append('setcode', set_selector.options[set_selector.selectedIndex].value);

		//Send Request with Form
		identify_card_request.open('POST', '/identify_card', true);
		identify_card_request.send(fd);

	} else {
		console.log('Camera Not Working, so cannot send image for identify');
	};
});

// ADD/REMOVE BUTTONS
//////////////////////////////////////////////////////////////////////////////
// Note: All buttons are disabled at start until a card is identifyed

// Add Buttons
for (let i = 0; i < addbuttons.length; i++) {
	let addbutton = addbuttons[i];

	let id = addbutton.id;

	//amount will be an integer string or 'all'
	let amount = parseInt(id.slice(3), 10);

	addbutton.addEventListener('click', function () {

		//get name of card from card_name element
		let card = card_name.innerHTML;

		//get exisiting textarea contents, split by line
		let lines = card_list.value.split('\n');

		//boolean to track whether or not a line has changed
		let existed = false;

		//check each line to see if card already exists, if so add to amount on that line
		//goes from bottom to top
		for (let i = lines.length - 1; i >= 0; i--) {
			let line = lines[i];

			//break if a sideboard line is reached
			if (line.includes('Sideboard:')) { break; };

			//parse info from line
			let existingAmount = parseInt(line.substr(0, line.indexOf(' ')), 10);
			let existingCard = line.substr(line.indexOf(' ') + 1);

			if ((existingCard == card) && (existingAmount > 0)) {
				//changing a line by increasing amount
				existed = true;

				//do nothing if amount is not a number
				if (Number.isNaN(amount)) {
					newAmount = existingAmount;
				} else {
					newAmount = existingAmount + amount;
				};
				// build new version of line, and replace in lines array.
				newLine = newAmount.toString(10) + ' ' + existingCard;
				lines[i] = newLine;

				//break after card is found
				break;
			};
		};
		//If doesn't already exist, Append new line to textarea
		if (!existed) {
			if (lines[lines.length - 1] == '') {
				card_list.value = lines.join('\n') + amount + ' ' + card;
			} else {
				card_list.value = lines.join('\n') + '\n' + amount + ' ' + card;
			}
			//Else just recombine the lines
		} else {
			card_list.value = lines.join('\n');
		};
	});
};

// Remove Buttons
for (let i = 0; i < removebuttons.length; i++) {
	let removebutton = removebuttons[i];

	let id = removebutton.id;

	//amount will be an integer string or 'all'
	let amount = parseInt(id.slice(3), 10);

	removebutton.addEventListener('click', function () {
		//get name of card from card_name element
		let card = card_name.innerHTML;

		//get exisiting textarea contents, split by line
		let lines = card_list.value.split('\n');

		//array to hold lines that should be deleted
		let deletes = [];

		//check each line to see if card already exists, if so delete the appropriate amount
		//goes from bottom to top
		for (let i = lines.length - 1; i >= 0; i--) {
			let line = lines[i];

			//break if a sideboard line is reached
			if (line.includes('Sideboard:')) { break; };

			// parse info from line
			let existingAmount = parseInt(line.substr(0, line.indexOf(' ')), 10);
			let existingCard = line.substr(line.indexOf(' ') + 1);

			if ((existingCard == card) && (existingAmount > 0)) {
				//changing a line by subtracting amount

				//remove all if amount is not an integer
				if (Number.isNaN(amount)) {
					newAmount = 0;
				} else {
					newAmount = existingAmount - amount;
				};

				// if new amount is 0 or negative, mark line for deletion
				if (newAmount < 1) {
					deletes.push(i);
				} else {
					// build new version of line, and replace in lines array.
					newLine = newAmount.toString(10) + ' ' + existingCard;
					lines[i] = newLine;
				}

				//break after card is found
				break;
			};
		};

		// remove lines marked for deletion
		newLines = [];
		for (let i = 0; i < lines.length; i++) {
			if (!(deletes.includes(i))) {
				newLines.push(lines[i]);
			};
		};

		//recombine the lines
		card_list.value = newLines.join('\n');
	});
};

// TEXT AREA BUTTONS
//////////////////////////////////////////////////////////////////////////////

//Clear button should empty all contents of text area
clear_button.addEventListener('click', function () {
	if (confirm('Are you sure you want to clear the text area?')) {
		card_list.value = '';
	};
});

//start sideboard button
sideboard_button.addEventListener('click', function () {
	card_list.value = card_list.value + '\n\nSideboard:';
});

//button to save contents to file
save_button.addEventListener('click', function () {

	//create blob with textarea contents
	let toWrite = new Blob([card_list.value], { type: "text/plain;charset=utf-8" });
	//use FileSaver.js to save to file
	saveAs(toWrite, 'decklist.txt');
});