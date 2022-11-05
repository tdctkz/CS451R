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

function myFunction() {
  var input, filter, ul, li, a, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  ul = document.getElementById("myUL");
  card = ul.getElementsByTagName("card");
  for (i = 0; i < card.length; i++) {
    a = card[i].getElementsByTagName("a")[0];
    txtValue = a.textContent || a.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      card[i].style.display = "";
    } else {
      card[i].style.display = "none";
    }
  }
}

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
