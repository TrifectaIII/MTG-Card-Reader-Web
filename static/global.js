// Global JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

// GLOBAL FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////

//Disable all buttons stored in a dictionary
function disableButtons(nodeli) {
	for (let i = 0; i < nodeli.length; i++) {
		nodeli[i].disabled = true;
	};
};

//Enable all buttons stored in a dictionary
function enableButtons(nodeli) {
	for (let i = 0; i < nodeli.length; i++) {
		nodeli[i].disabled = false;
	};
};

//SETUP
//////////////////////////////////////////////////////////////////////////////

//Get HTML Elements

var cam_select = document.querySelector('.cam_select');//Selector for choosing video input
var webcam_feed = document.querySelector('.webcam_feed');//Video Element for Webcam Feed
var reload_cam_button = document.querySelector('.reload_cam_button')//button for reloading the video feed
var set_selector = document.querySelector('.set_selector');//Select Element to Choose Set
var card_image = document.querySelector('.card_image');//Image Element to Display Identified Card Image
var card_name = document.querySelector('.card_name');//Span to Display Identified Card Name
var card_link = document.querySelector('.card_link');//Span to house link to scryfall for this card
var identify_card_button = document.querySelector('.identify_card_button');//Button to Execute Identification
var card_list = document.querySelector('.card_list');//Text Area for generating list of cards
var clear_button = document.querySelector('.clear_button');//Button to clear text area
var sideboard_button = document.querySelector('.sideboard_button');//Button to start sideboard
var save_button = document.querySelector('.save_button');//Button to save contents of textarea to file

//NodeLists to Hold Adding Buttons
var addbuttons = document.querySelectorAll('.add_button');//NodeList of adding buttons
var removebuttons = document.querySelectorAll('.remove_button');//NodeList of remove buttons
var addremovebuttons = document.querySelectorAll('.remove_button, .add_button');//NodeList of add and remove buttons

//Global Variables
var cam_working = false;//boolean to track whether Webcam Feed is working
var sets_load = false;//boolean to track whether set selector has been populated
var set_selected = false;//boolean to track whether set has been selected
var identify_start = 0;//integer to help calculate response time of identify requests

//Preload Loading Card and Error Card Images
var plimg_load = new Image();
plimg_load.src = '/static/identifying.gif';
var plimg_error = new Image();
plimg_error.src = '/static/error.gif';