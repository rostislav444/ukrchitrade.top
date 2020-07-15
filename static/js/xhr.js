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

function XHR(method, url, data=null) {
    let request = new XMLHttpRequest();
    
    request.open(method, url, false);
    // request.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    request.setRequestHeader("Content-Type", "application/json");

;
    
    if (method.toUpperCase() == 'POST') {
        request.setRequestHeader("X-CSRFToken", getCookie('csrftoken')  );
    }
    request.send(JSON.stringify(data))
    if (request.status === 200) {
        let response = JSON.parse(request.responseText); 
        return response
    } else {
        return {'error' : 'error'}
    }
}