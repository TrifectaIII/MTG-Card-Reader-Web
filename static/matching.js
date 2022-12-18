// JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

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

		// response should be an sfid
		let identifiedSFID = identify_card_request.response.toString();
		let identifiedName = identify_card_request.response.toString();

		if (identifiedName.length == 0) {
			// If no identify is made, display error
			card_image.onload = function () {
                card_name.innerHTML = '&nbsp;';
                card_link.innerHTML = '&nbsp;';
                notify('Identification Error: Unable to identify card. Please ensure card is against a neutral background.');
                card_image.onlick = null;
			};
			card_image.src = '/static/error.gif';
		} else {
            
			// Display card image from URL and name from name
			card_image.onload = function () {
				// Display name and link only after image has loaded
                card_name.innerHTML = identifiedName;
                card_link.innerHTML = '<a target = "_blank" href="https://scryfall.com/card/' + identifiedSFID.toString() + '">Scryfall</a>';
				//Enable adding Buttons also after image has loaded
                enableButtons(addremovebuttons);
                //card itself links to scryfall page as well
                card_image.onclick = () => {
                    window.open('https://scryfall.com/card/'+identifiedSFID.toString(),'_blank');
                }
            };
            
			// scryfall (can change version in url)
			card_image.src = 'https://api.scryfall.com/cards/' + identifiedSFID.toString() + '/?format=image&version=border_crop';
		};
	} else {
        console.log('Request completed incorrectly. Error', identify_card_request.status);
        notify('Server Error: identify_card request failed on receipt. Please reload page and try again.');
	};
};

//Tell request what to do upon error
identify_card_request.onerror = function () {
	console.log("identify_card didn't work at all");

	//display error image
	card_image.onload = function () {
        card_name.innerHTML = '&nbsp;';
        card_link.innerHTML = '&nbsp;';
        notify('Server Error: identify_card request failed before receipt. Please reload page and try again.');
        card_image.onlick = null;
	};
	card_image.src = '/static/error.gif';

};

//Tell identify button to send request on click
identify_card_button.addEventListener('click', function () {
	if (cam_working) {

		//start response timer
		identify_start = Date.now();

		//Remove previous card and display loading
		card_image.onload = function () {
            card_name.innerHTML = '&nbsp;';
            card_link.innerHTML = '&nbsp;';
			//Disable all adding buttons until new card identifyed
            disableButtons(addremovebuttons);
		};
		card_image.src = '/static/identifying.gif';


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