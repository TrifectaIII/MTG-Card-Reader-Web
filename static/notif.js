// Notification Area Script for https://github.com/TrifectaIII/MTG-Card-Reader-Web

var notif = getById('notif');//Notification Pop-up
var notif_text = getById('notif_text');//Text in in Notification
var close_notif = getById('close_notif');//Button to close Notification
var open_notif = getById('open_notif');//Button to open Notification

// close_notif must close the notif
close_notif.addEventListener('click', function () {
    notif_text.innerHTML = '';
    notif.style.display = 'none';
});

//Global function for displaying notifications
var notify = function (message) {
    notif_text.innerHTML = message+'<br>';
    notif.style.display = 'block';
};

open_notif.addEventListener('click', function () {
    notify('This is a Test Notification');
});