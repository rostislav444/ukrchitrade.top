const searchBar = document.querySelector('input[type="search"]')

searchBar.oninput = () => {
    console.log(searchBar.value);
}