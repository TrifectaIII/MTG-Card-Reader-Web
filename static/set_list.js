// JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

// POPULATES SET LIST using choices.js
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
        notify('Server Error: set_list request failed on receipt. Please reload page and try again.');
	};
};

//Tell request what to do upon error
set_list_request.onerror = function () {
	console.log("set_list request failed");
	notify('Server Error: set_list request failed before receipt. Please reload page and try again.');
};

//send request targeting sets.json file
set_list_request.open('GET', '/static/sets.json', true);
set_list_request.send();