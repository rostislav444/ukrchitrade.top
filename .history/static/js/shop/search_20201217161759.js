const searchBar = document.querySelector('input[type="search"]')

var timeoutr = null;

function searchproducts() {
    console.log(searchBar.value);
    timeout = null
}





searchBar.oninput = () => {
    var that = this;
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () {
        searchproducts()
    }, 1000)
    
}