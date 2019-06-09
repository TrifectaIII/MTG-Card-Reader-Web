window.onload = function () {

	//SETUP
	/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

	//HTML elements
	var notif = document.getElementById('notif')//Text Area for Notifications
	var webcam_feed = document.getElementById("webcam_feed");//Video Element for Webcam Feed
	var set_selector = document.getElementById('set_selector');//Select Element to Choose Set
	var cardDisplay = document.getElementById('cardDisplay');//Image Element to Display Matched Card Image
	var cardName = document.getElementById('cardName');//Text Area to Display Matched Card Name
	var match_card_button = document.getElementById('match_card_button');//Button to Execute Matching

	//Global Variables
	var cam_working = false;//boolean to track whether Webcam Feed is working
	var sets_load = false;//boolean to track whether set selector has been populated
	var set_selected = false;//boolean to track whether set has been selected
	var match_start = 0;//integer to help calculate response time of match requests

	//Preload Loading Card and Error Card Images
	var plimg_load  = new Image();
	plimg_load.src  = '/static/loadingcard.png';
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
	}

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
			}
		}
	});

	//Create set_list Request Object
	var set_list_request = new XMLHttpRequest();

	//Tell request to populat set_selector element after recieving reponse
	set_list_request.onload = function () {
		if (set_list_request.status >= 200 && set_list_request.status < 400) {
			
			//Get full response as JSON
			let respJSON = JSON.parse(set_list_request.response);

			//Init List of Choice Objects
			let options = [];

			//for each set in JSON, add set to options
			for (let setcode in respJSON){
				let setname = respJSON[setcode];
				options.push({
					value:setcode,
					label:setname + ' ('+setcode+')',
					selected: false,
					disabled: false,
				})
			};

			//Add all set Choice objects to Choices element
			set_selector_choice.setChoices(options,'value','label',true);
			sets_load = true;
			
		} else {
			console.log('set_list request completed incorrectly. Error', set_list_request.status);
		}
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
			
			//Calculate Response Time and print to console
			console.log('Match_Card Response Time (s):',(Date.now()-match_start)/1000)


			//Get full response as JSON
			let respJSON = JSON.parse(match_card_request.response);

			//Access response for name and url
			let matchName = respJSON.name;
			let matchMVID = respJSON.mvid;

			if (matchName.length == 0){
				// If no match is made, display error
				cardDisplay.onload = function () {
					cardName.innerHTML = 'COULD NOT IDENTIFY CARD';
				cardName.style.backgroundColor = 'lightcoral';
				}
				cardDisplay.src = '/static/errorcard.png';
			} else {
				// Display card image from URL and name from name
				cardDisplay.onload = function () { // Display name only after image has loaded
					cardName.innerHTML = 'Card Name: ' + matchName;
				}
				cardDisplay.src = 'https://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+matchMVID+'&type=card';
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

			//start response timer
			match_start = Date.now()

			//Remove previous card and display loading
			cardDisplay.onload = function () {
				cardName.innerHTML = 'Loading...';
				cardName.style.backgroundColor = '';
			}
			cardDisplay.src = '/static/loadingcard.png';

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
