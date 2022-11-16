//NumberFormat
let x = document.querySelectorAll(".nums");
for (let i = 0, len = x.length; i < len; i++) {
  let num = Number(x[i].innerHTML)
    .toLocaleString('en');
  x[i].innerHTML = num;
  x[i].classList.add("currSign");
}


// Show password function /
function show_Password() {
  var x = document.getElementById("password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}


// Remember username funciton/
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

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})


function search_bar() {
  let input = document.getElementById('searchbar').value
  input = input.toLowerCase();
  let x = document.getElementsByClassName('card');

  for (i = 0; i < x.length; i++) {
    if (!x[i].innerHTML.toLowerCase().includes(input)) {
      x[i].style.display = "none";
    }
    else {
      x[i].style.display = "";
    }
  }
}

var myInput = document.getElementById("pwd");
var symbol = document.getElementById("symbol");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");

// When the user clicks on the password field, show the message box
myInput.onfocus = function () {
  document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function () {
  document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the password field
myInput.onkeyup = function () {
  // Validate lowercase letters
  var symbol = /[!@#$%^&*()_+.?]/g;
  if (myInput.value.match(symbol)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if (myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if (myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }

  // Validate length
  if (myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
}