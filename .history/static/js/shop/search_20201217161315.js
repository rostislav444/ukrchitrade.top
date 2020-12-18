const searchBar = document.querySelector('input[type="search"]')

var timer = null;

function searchproducts() {
    console.log(searchBar.value);
}

searchBar.oninput = () => {
    
    clearTimeout(timer);
    timer = setTimeout(searchproducts(), 600);
    

}