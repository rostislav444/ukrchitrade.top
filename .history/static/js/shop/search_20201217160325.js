const searchBar = document.querySelector('input[type="search"]')

function searchproducts() {
    console.log(searchBar.value);
}


searchBar.oninput = () => {
    
    setTimeout(searchproducts(), 1000);
}