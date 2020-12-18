from apps.catalogue.models import Product
from project import settings


class WatchList(object):
    def __init__(self, request):
        self.session = request.session
        watchlist = self.session.get(settings.WATCHLIST_SESSION_ID)
        if not watchlist:
            watchlist = self.session[settings.WATCHLIST_SESSION_ID] = []
        self.watchlist = watchlist

    def __iter__(self):
        for item in self.watchlist:
            yield item

    def save(self):
        self.session.modified = True

    def add(self, product_id):
        id = int(product_id)
        watchlist = self.watchlist
        if id in watchlist:
            watchlist.remove(id)
        watchlist.insert(0, id)
        self.watchlist = watchlist
        self.save()
        return self.data()

    def data(self):
        exclude, product_list = [], []
        products = Product.objects.filter(pk__in=self.watchlist)
        for product_id in self.watchlist:
            try:
                product_list.append(products.get(pk=int(product_id))) 
            except:
                exclude.append(product_id)
        return product_list