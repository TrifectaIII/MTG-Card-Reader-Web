// Modal Box Window Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web */


var modal = document.querySelector('.modal');
var closeButtons = document.querySelectorAll('.close-modal');
var openButton = document.querySelector('.open-modal');
var inner = document.querySelector('.modal-inner')
var content = document.querySelector('.modal-content')

// set open modal behaviour
openButton.addEventListener('click', function () {
    modal.classList.toggle('modal-open');
    // document.body.scrollTop = document.documentElement.scrollTop = 0;
});

// set close modal behaviour
for (i = 0; i < closeButtons.length; ++i) {
    closeButtons[i].addEventListener('click', function () {
        modal.classList.toggle('modal-open');
    });
}

// close modal if clicked outside content area
inner.addEventListener('click', function () {
    modal.classList.toggle('modal-open');
});

// prevent modal inner from closing parent when clicked
content.addEventListener('click', function (e) {
    e.stopPropagation();
});