const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
    timer = null
}





searchBar.oninput = () => {
    
    timer = setTimeout(() => {searchproducts()} , 500);
}