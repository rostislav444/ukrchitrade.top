const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
}



if (timer != null) {
  window.clearTimeout(timer); 
  timer = null;
}
else {
  timer = window.setTimeout(yourFunction, 0);
}

searchBar.oninput = () => {
    console.log(timer);
    timer = setTimeout(() => {searchproducts()} , 500);
}