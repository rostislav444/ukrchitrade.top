function Checked() {
    var tBody = document.querySelector('tbody')
    let checkboxes = tBody.querySelectorAll('input[type=checkbox]')
    if (checkboxes.length == 0) {
      alert('Нет товаров для выбора')
      return false
    }

    let checked = []

    for (let i = 0; i < checkboxes.length; i++) {
      let checkbox = checkboxes[i]
      let node = checkbox
      if (node.checked) {
        while (true) {
          if (node.nodeName == 'TR') {
            checked.push(node.dataset.id)
            break
          }
          node = node.parentNode
        }
      }
    }
    return checked
  }