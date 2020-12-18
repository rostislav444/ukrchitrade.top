const watchlist_wrapper = document.querySelector('.watchlist_wrapper')
const watchlist_products = document.querySelector('.watchlist_products')


function WatchListSwiper() {
    var WatchList = new Swiper('.watchlist', {
        loop: false,
        slidesPerView: 4,
        slidesPerGroup: 1,
        pagination:  {el: '.swiper-pagination' },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        scrollbar: {
            el: '.swiper-scrollbar',
        },
    })
    
}

function setWatchList(data) {
    html = data['html']
    length = data['length']
    if (length > 0) {
        watchlist_products.innerHTML = html
        watchlist_wrapper.style.display = 'block'
        WatchListSwiper()
    }
}

XHR('GET', watchlist_url, data={}, setWatchList)