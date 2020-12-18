const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
}

searchBar.oninput = () => {
    if (timer != null) {
        window.clearTimeout(timer); 
        timer = null;
    } else {
        timer = window.setTimeout(() => {searchproducts()}, 500);
    }
    // timer = setTimeout(() => {searchproducts()} , 500);
}