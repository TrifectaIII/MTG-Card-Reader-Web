// Primary JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

window.onload = function () {

	//SETUP
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Get HTML Elements
	var notif = document.getElementById('notif');//Text Area for Notifications
	var webcam_feed = document.getElementById("webcam_feed");//Video Element for Webcam Feed
	var set_selector = document.getElementById('set_selector');//Select Element to Choose Set
	var card_display = document.getElementById('card_display');//Image Element to Display Matched Card Image
	var card_name = document.getElementById('card_name');//Text Area to Display Matched Card Name
	var match_card_button = document.getElementById('match_card_button');//Button to Execute Matching
	var card_list = document.getElementById('match_card_button');//Text Area for generating list of cards

	//Dictionary to Hold Adding Buttons
	addingButtonDict = {};
	//List of Adding Button Id's
	var idList = ['add1','add4','add10','rem1','rem4','rem10','remall'];
	//Loop through list and add to dict with id as key
	for (let i=0; i < idList.length; i++){
		let id = idList[i];
		addingButtonDict[id] = document.getElementById(id);
	};

	//Start with all buttons disabled, before any card is matched
	disableButtons(addingButtonDict);

	//Global Variables
	var cam_working = false;//boolean to track whether Webcam Feed is working
	var sets_load = false;//boolean to track whether set selector has been populated
	var set_selected = false;//boolean to track whether set has been selected
	var match_start = 0;//integer to help calculate response time of match requests

	//Preload Loading Card and Error Card Images
	var plimg_load  = new Image();
	plimg_load.src  = '/static/loadingcard.gif';
	var plimg_error = new Image();
	plimg_error.src = '/static/errorcard.png';
	
	// WEBCAM
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Access User's Webcam and feed to webcam_feed Element
	if (navigator.mediaDevices.getUserMedia) {
		navigator.mediaDevices.getUserMedia({ video: true })
			.then(function (stream) {
				//If Cam is Working
				webcam_feed.srcObject = stream;
				cam_working = true;
				notif.innerHTML = "Webcam Functional";

				//Enable match button once set is selected and camera is working
				if (set_selected){
					match_card_button.disabled = false;
				}
			})
			.catch(function (err0r) {
				//If Cam Fails
				console.log("Something went wrong!",err0r);
				cam_working = false;
				notif.innerHTML = "Webcam Error: Please ensure camera is connected and that this page has permission to use it. Then reload page.";
				notif.style.backgroundColor = 'lightcoral';
			});
	};

	// POPULATE SET LIST
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Turn set_selector into Choices element
	var set_selector_choice = new Choices(set_selector,{
		//Options for Choices element
		addItems: true,
		removeItems: false,
		renderChoiceLimit: -1,
		searchResultLimit: 5,
		searchPlaceholderValue:"Search by Set Name or Code:",
		itemSelectText:'',
	});

	//Enable match button once set is selected and camera is working
	set_selector.addEventListener('choice', function(){
		if (sets_load){
			set_selected = true;
			if (cam_working){
				match_card_button.disabled = false;
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
			for (let setcode in respJSON){
				let setname = respJSON[setcode];
				choiceList.push({
					value:setcode,
					label:setname + ' ('+setcode+')',
					selected: false,
					disabled: false,
				});
			};

			//Add all set Choice objects to Choices element
			set_selector_choice.setChoices(choiceList,'value','label',true);
			sets_load = true;
			
		} else {
			console.log('set_list request completed incorrectly. Error', set_list_request.status);
		};
	};

	//Tell request what to do upon error
	set_list_request.onerror = function () {
		console.log("set_list didn't work at all");
	};

	//send request targeting sets.json file
	set_list_request.open('GET', '/static/sets.json', true);
	set_list_request.send();

	// MATCHING SYSTEM
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//Create Canvas Object for Temporary Image Processing
	var temp_canvas = document.createElement("CANVAS");
	var temp_context = temp_canvas.getContext('2d');

	//Create set_list Request Object
	var match_card_request = new XMLHttpRequest();

	//Tell request to display card after recieving reponse
	match_card_request.onload = function () {
		if (match_card_request.status >= 200 && match_card_request.status < 400) {
			
			//Calculate Response Time and log to console
			console.log('Match_Card Response Time (s):',(Date.now()-match_start)/1000);

			//Get full response as JSON
			let respJSON = JSON.parse(match_card_request.response);

			//Access response for name and url
			let matchName = respJSON.name;
			let matchMVID = respJSON.mvid;

			if (matchName.length == 0){
				// If no match is made, display error
				card_display.onload = function () {
					card_name.innerHTML = 'COULD NOT IDENTIFY CARD';
				card_name.style.backgroundColor = 'lightcoral';
				};
				card_display.src = '/static/errorcard.png';
			} else {
				// Display card image from URL and name from name
				card_display.onload = function () { // Display name only after image has loaded
					card_name.innerHTML = matchName;
				};
				card_display.src = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+matchMVID+'&type=card';
				//Enable adding Buttons
				enableButtons(addingButtonDict);
			};
		} else {
			console.log('Request completed incorrectly. Error', match_card_request.status);
		};
	};

	//Tell request what to do upon error
	match_card_request.onerror = function () {
		console.log("match_card didn't work at all");
	};

	//Tell match button to send request on click
	match_card_button.onclick = function () {
		if (cam_working) {

			//start response timer
			match_start = Date.now();

			//Remove previous card and display loading
			card_display.onload = function () {
				card_name.innerHTML = 'Loading...';
				card_name.style.backgroundColor = '';
			};
			card_display.src = '/static/loadingcard.gif';

			//Disable all adding buttons until new card matched
			disableButtons(addingButtonDict);

			//Capture image from webcam feed to temp canvas
			let vid_width = webcam_feed.videoWidth;
			let vid_height = webcam_feed.videoHeight;
			temp_canvas.width = vid_width;
			temp_canvas.height = vid_height;
			temp_context.drawImage(webcam_feed, 0, 0, vid_width, vid_height);

			//Convert temp canvas image to PNG/JPG Data
			let capture = temp_canvas.toDataURL("image/jpeg",0.1); //Send as JPG, numeric argument is quality (higher is better quality)
			//let capture = temp_canvas.toDataURL("image/png"); //Send as PNG

			//Create Form Data Object to send with Request
			let fd = new FormData();

			//Append PNG Data to Form
			fd.append('image', capture);

			//Append Setcode to Form
			fd.append('setcode', set_selector.options[set_selector.selectedIndex].value);

			//Send Request with Form
			match_card_request.open('POST', '/match_card', true);
			match_card_request.send(fd);

		} else {
			console.log('Camera Not Working, so cannot send image for match');
		};
	};
};

//Disable all buttons stored in a dictionary
var disableButtons = function (dict) {
	for (let id in dict) {
		dict[id].disabled = true;
	}
}

//Enable all buttons stored in a dictionary
var enableButtons = function (dict) {
	for (let id in dict) {
		dict[id].disabled = false;
	}
}