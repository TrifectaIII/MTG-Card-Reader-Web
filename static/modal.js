// MODAL
var modal = document.querySelector('.modal');
var closeButtons = document.querySelectorAll('.close-modal');
// set open modal behaviour
document.querySelector('.open-modal').addEventListener('click', function() {
    modal.classList.toggle('modal-open');
    // document.body.scrollTop = document.documentElement.scrollTop = 0;
});
// set close modal behaviour
for (i = 0; i < closeButtons.length; ++i) {
closeButtons[i].addEventListener('click', function() {
        modal.classList.toggle('modal-open');
    });
}
// close modal if clicked outside content area
document.querySelector('.modal-inner').addEventListener('click', function() {
    modal.classList.toggle('modal-open');
});
// prevent modal inner from closing parent when clicked
document.querySelector('.modal-content').addEventListener('click', function(e) {
    e.stopPropagation();
});