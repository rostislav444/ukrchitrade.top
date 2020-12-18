function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function XHR(method, url, data, func, params) {
    let csrf = getCookie("csrftoken")
    console.log(url, csrf);
    let request = new XMLHttpRequest();
        request.open(method, url, true);
        request.setRequestHeader("Content-Type", "application/json");
        request.setRequestHeader("X-CSRFToken", csrf);
        request.send(data)
        request.onload = () => {
            // console.log(request.responseText);
            func(JSON.parse(request.responseText), params)
        }
       
     

}