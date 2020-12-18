const searchBar = document.querySelector('input[type="search"]')

function searchproducts() {
    console.log(searchBar.value);
}


searchBar.oninput = () => {
    
    setTimeout(sayHi(), 1000);
}