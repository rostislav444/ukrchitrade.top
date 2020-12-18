const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
    timer = null
}





searchBar.oninput = () => {
    var that = this;
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () {
        searchproducts()
    }, 100
    
}