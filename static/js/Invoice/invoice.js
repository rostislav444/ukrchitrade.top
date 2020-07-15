// INVOICE
var selectInvoice = document.getElementById('select_invoice')

function InvoiceReInit() {
    InvoiceEventListener()
    InvoiceProductQuantityChange()
    InvoiceProductCheckBox()
}



function RenderInvoice(response) {
    var invoice = document.querySelector('#invoice_form')
    let tpl = nunjucks.renderString(document.querySelector('#tpl_invoice').innerHTML, {'invoice' : response['invoice'] })
    invoice.innerHTML = tpl   
    $('.date').datepicker({format: 'dd.mm.yyyy',});
    document.getElementById('selected-products').innerHTML = document.getElementById('invoice_products').innerHTML
    InvoiceReInit()
}

// FETCH INVOICE DATA
function FetchInvoiceData(id=0) {
    let response = XHR(method='GET', urlInvoiceGet + id + '/', data=null)
    response = JSON.parse(response)
    RenderInvoice(response)
}FetchInvoiceData()


// ADD INVOICE EVENT LISTENTER
function InvoiceEventListener() {
    selectInvoice = document.getElementById('select_invoice')
    selectInvoice.addEventListener('change', function(){
        let option = selectInvoice.querySelector('option:checked') 
        let value = parseInt(option.value)
        FetchInvoiceData(value)
    })
} 

// DOWNLOAD INVOICE
function printInvoice() {
    function download(url,filename) {
        var element = document.createElement('a');
        element.setAttribute('href', url);
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    let selectInvoice = document.getElementById('select_invoice')
    let option = selectInvoice.querySelector('option:checked') 
    let value = parseInt(option.value)
    let url = urlInvoicePrint + value + '/'
    let response = XHR(method='GET', url, data=null)
    download(response['url'],response['filename'])
    console.log(response['url']);
    
}

// DLETE PRODUCT
function InvoiceProductDelete(obj) {
    document.querySelectorAll('.' + obj.dataset.parent).forEach(el => el.remove());
}

// DLETE PRODUCT
function InvoiceDelete(id) {
    document.querySelectorAll('.' + obj.dataset.parent).forEach(el => el.remove());
}

// CHECKBOX
function InvoiceProductCheckBox() {    
    let checkboxes = document.querySelectorAll('.product-checkbox')
    for (let i = 0; i < checkboxes.length; i++) {
        let checkbox = checkboxes[i];
        checkbox.onchange = function() {
            let tableRowChaeckbox = document.getElementsByClassName(checkbox.dataset.id)
            for (let input of tableRowChaeckbox ) {
                if (tableRowChaeckbox !== undefined) {
                    input.checked = checkbox.checked
                }
            }
            
        }
    }
}

// QUANTITY CHANGE
function InvoiceProductQuantityChange() {
    let inputs = document.querySelectorAll('.invoice-product-input')
    for (let i = 0; i < inputs.length; i++) {
        let el = inputs[i];
        el.onchange = function() {
            let inputsToChange = document.querySelectorAll('.' + el.dataset.parentclass)
            for (let input of inputsToChange ) {
                    let numberInput = input.querySelector('input[type="number"]')
                    numberInput.value = el.value
                    
            }
        }
    }
} InvoiceProductQuantityChange()






var selectInvoice = document.getElementById('select_invoice')
var invoiceButton = document.getElementById('invoice_button')
var products = document.querySelectorAll('.product_qty')

function Invoice() {
    data = {'products' : []}

    // InvoiceFields
    let invoiceFields = document.querySelectorAll('.infoice-form-field')
    for (let i = 0; i < invoiceFields.length; i++) {
        let field = invoiceFields[i];
        if (field.tagName == 'SELECT') {
            let options = field.querySelectorAll('option')
            for (let j = 0; j < options.length; j++) {
                let option = options[j];
                if(option.selected == true) {
                    data[field.name] = option.value
                }
            } 
        } 
        if (field.tagName == 'INPUT') {
            data[field.name] = field.value
        } 
    }
    
    // InvoiceProducts
    let invoiceProductsList = document.querySelector('#invoice_products')
    let invoiceProducts = invoiceProductsList.querySelectorAll('.invoice-product-input')

    for (let i = 0; i < invoiceProducts.length; i++) {
        let product = invoiceProducts[i];
        
        
        data['products'].push({'id' : product.dataset.id, 'quantity' : product.value})
    }

    console.log('123',data['products']);

    if (parseInt(data['id']) >= 0) {
        url = urlInvoiceUpdate + data['id'] + '/'
    } else {
        alert('Incorect id')
        return
    }
    data = JSON.stringify(data)
    let response = XHR(method='POST', url, data)
    response = JSON.parse(response)

    if ('error' in response) {
        alert(response['error'])
    } else if ('invoice' in response) {
        RenderInvoice(response)
    } else {
        alert('Ошибка')
    }
    
    
}   




