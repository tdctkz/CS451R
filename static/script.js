/ Delete notes function/
function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

/ Show password function /
function show_Password() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function password_show_hide() {
  var x = document.getElementById("password1");
  var show_eye = document.getElementById("show_eye");
  var hide_eye = document.getElementById("hide_eye");
  hide_eye.classList.remove("d-none");
  if (x.type === "password") {
    x.type = "text";
    show_eye.style.display = "none";
    hide_eye.style.display = "block";
  } else {
    x.type = "password";
    show_eye.style.display = "block";
    hide_eye.style.display = "none";
  }
}

/ Remember username funciton/
const rmCheck = document.getElementById("rememberMe"),
  username_input = document.getElementById("username");

if (localStorage.checkbox && localStorage.checkbox !== "") {
  rmCheck.setAttribute("checked", "checked");
  username_input.value = localStorage.username;
} else {
  rmCheck.removeAttribute("checked");
  username_input.value = "";
}

function lsRememberMe() {
  if (rmCheck.checked && username_input.value !== "") {
    localStorage.username = username_input.value;
    localStorage.checkbox = rmCheck.value;
  } else {
    localStorage.username = "";
    localStorage.checkbox = "";
  }
}

var source = new EventSource("/progress");
source.onmessage = function (event) {
  $('.progress-bar').css('width', event.data + '%').attr('aria-valuenow', event.data);
  $('.progress-bar-label').text(event.data + '%');

  if (event.data == 100) {
    source.close()
  }
}