from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from apps.shop.models import Product, Variant
from apps.comments.models import Comment, CommentLike, CommentImages
from apps.core.functions.functions__validators import checkPhone, checkEmail, check_phone_email
from apps.user.models import CustomUser
from django.db.models import Q




@require_http_methods(["POST","GET"])
def comments(request, product_id):
    product = Product.objects.get(pk=product_id)
    
    if request.method == "POST":
        data = request.POST
        email, phone = check_phone_email(username=data['username'], request=request)

        if all(var is None for var in [email, phone]):
            response = {'msg' : 'Введите корректный номер Телефона или Email' }
            return JsonResponse(response)
    
        try: 
            if   email: user = CustomUser.objects.get(email=email)
            elif phone: user = CustomUser.objects.get(phone=phone)
        except:  
            user = CustomUser.objects.create_user(username=data['username'], data=data, request=request)
            if isinstance(user, CustomUser) == False:
                response = {'msg' : user }
                return JsonResponse(response)

        # SAVE REVIEW
        review = Comment(parent=product, stars=int(data['stars']), user=user, text=data['text'])
        review.save()
        # SAVE IMAGES
        images = request.FILES.getlist('image')
        if len(images) > 0:
            for image in images:
                reviewImage = CommentImages(parent=review, image_l=image)
                reviewImage.save()
    
        # TELEGRAM
        # msg = 'Комментарий: ' + variant.get_absolute_url() + '\n'
        # msg += data['text']
        # msg = urllib.parse.quote(msg)
        # url = "https://api.telegram.org/bot817785032:AAG-Q3s8wRhyZbkoJScSPvE2XDrCVlgZKKA/sendMessage?chat_id=-1001490724377&text=" + msg
        # contents = urllib.request.urlopen(url).read() 
   
    response = {'html' : '' }
    return JsonResponse(response)


def comment_likes(request, product_id, comment_id, like):
    
    if request.user.is_authenticated:
        like = True if like == 'like' else False
        try:    
            comment_like = CommentLike.objects.get(user=request.user, parent__pk=int(comment_id))
        except: 
            comment = Comment.objects.get(pk=int(comment_id))
            comment_like = CommentLike(user=request.user, parent=comment)
        comment_like.like = like
        print('LIKE IS', comment_like.like)
        comment_like.save()
    return redirect(request.META.get('HTTP_REFERER'))