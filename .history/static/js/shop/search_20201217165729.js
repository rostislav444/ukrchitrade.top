const searchBar = document.querySelector('input[type="search"]')

var timeout = null;

function SearchOutputRender(data) {
    console.log(data);
}

function searchproducts() {
    let url = cartUrls['search']
    data = {
        param : searchBar.value
    }
    XHR('POST', url, JSON.stringify(data), func=SearchOutputRender)
}


searchBar.oninput = () => {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () { searchproducts() }, 500)
}