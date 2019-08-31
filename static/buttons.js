// JS Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

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