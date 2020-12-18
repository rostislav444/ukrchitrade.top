from django.shortcuts import render, redirect
from django.urls import reverse
from apps.catalogue.models import Product, Category
from apps.shop.watchlist import WatchList
from apps.comments.models import Comment, Question
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from project import settings








class ProductPage(viewsets.ViewSet):
    context = {}
    permission_classes = [AllowAny]


    def redirect_to_product(self, product, variant=None, page=None, api=None):
        kwargs = {
            'slug':product.slug, 
            'category':product.category_tree_slug, 
            'product_id':product.pk,
        }
        if variant: kwargs['variant_id'] = variant.pk
        if page:    kwargs['page'] = page
        return redirect(reverse('shop:product', kwargs=kwargs))


    def get_product(self, product_id, variant_id=None):
        product = Product.objects.get(pk=product_id)
        self.context = {'product' : product,}
        return product

    def create_commet(self, request):
        data = request.data
        commnent = Comment(
            user = request.user,
            product = product,
            rate = int(data['rate']),
            text = data['text'],
            text_plus = data['text_plus'],
            text_minus = data['text_minus'],
        )
        commnent.save()
        return commnent


    # PAGES
    def page(self, request, category, slug, product_id, page=None, api=False):
        product = self.get_product(product_id)
        self.context['page'] = page
        watchlist = WatchList(request)
        watchlist.add(product_id)

       
        if page in ['comment_form', 'question_form']:
            if request.user.is_authenticated == False:
                return redirect(reverse('user:login')+'?redirect='+request.path)
            if request.method == 'POST':
                if page == 'comment_form':
                    self.create_commet(request)
                    return redirect(reverse(
                        'shop:product', kwargs={'slug':product.slug, 'category':product.category.slug, 'product_id':product.pk, 'page':'comments'}
                    ))
                elif page == 'question_form':
                    pass

       
        if request.user.is_authenticated == False:
            Product.objects.filter(pk=product.pk).update(view=product.view+1)
        return render(request, 'shop/product/product__page.html', self.context)


    # COMMWNTS
    def comment_form(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect(reverse('user:login')+'?redirect='+request.path)
        product = self.get_product(kwargs.get('product_id'))
        if request.method == 'POST':
            data = request.data
            commnent = Comment(
                user = request.user,
                product = product,
                rate = int(data['rate']),
                text = data['text'],
                advantages = data['advantages'],
                disadvantages = data['disadvantages'],
            )
            commnent.save()
            return redirect(reverse(
                'shop:product', kwargs={'slug':product.slug, 'category':product.category.slug, 'product_id':product.pk, 'page':'comments'}
            ))
        return render(request, 'shop/product/pages/page__comment_form.html', self.context)

    def comment_reply(self, request, *args, **kwargs):
        return render(request, 'shop/product/pages/comments__page.html', self.context)


    # QUESTIONS
    def question_form(self, request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect(reverse('user:login'))
        product = self.get_product(kwargs.get('product_id'))
        if request.method == 'POST':
            data = request.data
            question = Question(
                user = request.user,
                product = product,
                text = data['text'],
            )
            question.save()
            return redirect(reverse(
                'shop:product', kwargs={'slug':product.slug, 'category':product.category_tree_slug, 'product_id':product.pk, 'page':'questions'}
            ))
        return render(request, 'shop/product/pages/questions__form.html', self.context)
    
    def question_reply(self, request, *args, **kwargs):
        return render(request, 'shop/product/pages/question__page.html', self.context)






