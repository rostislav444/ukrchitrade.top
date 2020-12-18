const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
}

searchBar.oninput = () => {
    var startTimer = function() {
        clearTimeout(timer);
        timer = setTimeout(DoThis, 6000);
    }

}