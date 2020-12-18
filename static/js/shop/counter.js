function Counter() {
    for (let counter of document.querySelectorAll('.counter')) {
        let actions = counter.querySelectorAll('.action')
        let input = counter.querySelector('input')

        function multiplyPrice(quantity) {
            if (quantity <= input.max && quantity >= input.min) {
                input.value = quantity
                
                if (input.dataset.priceClass) {
                    for (let price of document.getElementsByClassName(input.dataset.priceClass)) {
                        price.innerHTML = parseInt(price.dataset.value) * parseInt(quantity)
                    }
                }

                if (input.dataset.cartUpdate == "true") {
                    CartUpdate(input)
                }
                
            } 
            else if (quantity > input.max) { input.value = 100 } 
            else { input.value = 1 }
        } 

        for (let action of actions) {
            action.onclick = () => {
                if (action.classList.contains('plus'))  { multiplyPrice(parseInt(input.value) + 1) }
                if (action.classList.contains('minus')) { multiplyPrice(parseInt(input.value) - 1) }
            }
        }
        input.oninput = () => { multiplyPrice(parseInt(input.value)) }

        input.onchange = () => {}
    }
} Counter()


