function Close(id) {
    let conteiner = document.getElementById(id)
    // conteiner.classList.remove('active')
    conteiner.style.display = 'none'
}

function SimpleOpen(id) {
    let conteiner = document.getElementById(id)    
    conteiner.style.display = 'flex'
}

function Open(id, obj) {
    let conteiner = document.getElementById(id)
    if (obj.childNodes != undefined) {
        var childs = Array.prototype.slice.call(obj.childNodes)
    } else {
        var childs = []
    }
    childs.push(obj)

    var listener = function (event) {
        let conteiner = document.getElementById(id)
        let isClickInside = conteiner.contains(event.target);
        if (isClickInside == false && childs.includes(event.target) == false) {
            // conteiner.classList.remove('active')
            document.removeEventListener('click', listener, true);
        } 
    }  
    if (conteiner.classList.contains('active') == false) {
        conteiner.classList.add('active')
        document.addEventListener('click', listener, true)
    } else {
        conteiner.classList.remove('active')
        document.removeEventListener('click', listener, true);
    }
}

// while (el.parentNode) {
//     el = el.parentNode;
//     if (el.matches && el.matches(selector)) {
//         return el;
//     }
// }

