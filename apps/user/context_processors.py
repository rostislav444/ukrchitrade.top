from apps.user.models import CustomUser, Wishlist


def use(request):
    user = None
    if request.user.is_authenticated:
       user = request.user
    return {'user' : user} 


def wishlist(request):
    user = request.user
    if user.is_authenticated:
        return {'wishlist' :  user.products.all()}
    return {'wishlist' : []}
