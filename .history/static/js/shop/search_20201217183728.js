const searchBar = document.querySelector('input[type="search"]')
const searchPopUp = document.querySelector('.search_popup')
var timeout = null;


function showSearch() {

}
function hideSearch() {
    
}



function SearchOutputRender(data) {
    html = data['html']
    searchPopUp.innerHTML = html
}

function searchproducts() {
    let url = cartUrls['search']
    data = JSON.stringify({param : searchBar.value})
    XHR('POST', url, data, func=SearchOutputRender)
}


searchBar.oninput = () => {
    if (timeout !== null) {
        clearTimeout(timeout);
    }
    timeout = setTimeout(function () { searchproducts() }, 500)
}