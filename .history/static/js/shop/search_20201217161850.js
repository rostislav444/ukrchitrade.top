const searchBar = document.querySelector('input[type="search"]')

var timeout = null;

function searchproducts() {
    console.log(searchBar.value);
}





searchBar.oninput = () => {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () {
        searchproducts()
    }, 500)
    
}