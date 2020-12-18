const searchBar = document.querySelector('input[type="search"]')

var timeout = null;

function SearchOutputRender(data) {
    html = data['html']
    
}

function searchproducts() {
    let url = cartUrls['search']
    data = {
        'param' : searchBar.value
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=SearchOutputRender)
}


searchBar.oninput = () => {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () { searchproducts() }, 500)
}