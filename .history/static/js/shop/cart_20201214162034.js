var timer


function CartRender(data) {
    side_cart_products.innerHTML = data['html']
    side_cart.querySelector('.cart_total').innerHTML = data['total']
    openCart()
    Counter()
}


function CartAdd(input) {
    let url = cartUrls['cart_add']
    data = {
        product_id : input.dataset.product_id,
        quantity :   input.value,
        update:     false,
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=CartRender)
}
function CartAddID(id) {
    let url = cartUrls['cart_add']
    data = {
        product_id : id,
        quantity :   1,
        update:     false,
    }
    data = JSON.stringify(data)
    popupClose()
    XHR('POST', url, data, func=CartRender)
}

function CartUpdate(input) {
    let url = cartUrls['cart_add']
    data = {
        product_id : input.dataset.product_id,
        quantity :   input.value,
        update:     true,
    }
    data = JSON.stringify(data)
    XHR('POST', url, data, func=CartRender)
}