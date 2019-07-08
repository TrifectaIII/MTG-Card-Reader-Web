// Global JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

// GLOBAL FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////

//Disable all buttons stored in a dictionary
var disableButtons = function (nodeli) {
	for (let i = 0; i < nodeli.length; i++) {
		nodeli[i].disabled = true;
	};
};

//Enable all buttons stored in a dictionary
var enableButtons = function (nodeli) {
	for (let i = 0; i < nodeli.length; i++) {
		nodeli[i].disabled = false;
	};
};

//Wrapper Function for getElementById
var getById = function (id) {
	return document.getElementById(id);
};

var queryAll = function (cssMatch) {
    return document.querySelectorAll(cssMatch);
}

//SETUP
//////////////////////////////////////////////////////////////////////////////

//Get HTML Elements

var cam_select = getById('cam_select');//Selector for choosing video input
var webcam_feed = getById("webcam_feed");//Video Element for Webcam Feed
var reload_cam_button = getById('reload_cam_button')//button for reloading the video feed
var set_selector = getById('set_selector');//Select Element to Choose Set
var card_image = getById('card_image');//Image Element to Display Identified Card Image
var card_name = getById('card_name');//Text Area to Display Identified Card Name
var identify_card_button = getById('identify_card_button');//Button to Execute Identification
var card_list = getById('card_list');//Text Area for generating list of cards
var clear_button = getById('clear_button');//Button to clear text area
var sideboard_button = getById('sideboard_button');//Button to start sideboard
var save_button = getById('save_button');//Button to save contents of textarea to file

//NodeLists to Hold Adding Buttons
var addbuttons = queryAll('.add_button');//NodeList of adding buttons
var removebuttons = queryAll('.remove_button');//NodeList of remove buttons
var addremovebuttons = queryAll('.remove_button, .add_button');//NodeList of add and remove buttons

//Global Variables
var cam_working = false;//boolean to track whether Webcam Feed is working
var sets_load = false;//boolean to track whether set selector has been populated
var set_selected = false;//boolean to track whether set has been selected
var identify_start = 0;//integer to help calculate response time of identify requests

//Preload Loading Card and Error Card Images
var plimg_load  = new Image();
plimg_load.src  = '/static/loadingcard.gif';
var plimg_error = new Image();
plimg_error.src = '/static/errorcard.png';