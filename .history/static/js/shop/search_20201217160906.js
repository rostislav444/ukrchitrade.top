const searchBar = document.querySelector('input[type="search"]')

var timer

function searchproducts() {
    console.log(searchBar.value);
}


searchBar.oninput = () => {
    print(timer)
    timer = setTimeout(() => {searchproducts()} , 500);
}