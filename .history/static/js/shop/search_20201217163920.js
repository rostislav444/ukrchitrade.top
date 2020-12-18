const searchBar = document.querySelector('input[type="search"]')

var timeout = null;

function searchproducts() {
    let url = cartUrls['search']
    console.log();

    
    data = {search : searchBar.value}
    XHR('POST', url, data, func=CartRender)
}


searchBar.oninput = () => {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () {
        searchproducts()
    }, 500)
    
}