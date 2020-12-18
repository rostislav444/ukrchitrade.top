const searchBar = document.querySelector('input[type="search"]')

var timer

function searchproducts() {
    console.log(searchBar.value);
}


searchBar.oninput = () => {
    
    setTimeout(() => {searchproducts()} , 10000);
}