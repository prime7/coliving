from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from .models import Store, Product, Cart, CartProduct
from config.functions import verify_address

class BusinessIndex(ListView):
    paginate_by = 25
    model = Store

    def get(self, request, *args, **kwargs):
        stores = Store.objects.all()

        paginator = Paginator(stores, self.paginate_by)

        page = request.GET.get('page')

        try:
            posting_paginations = paginator.page(page)
        except PageNotAnInteger:
            posting_paginations = paginator.page(1)
        except EmptyPage:
            posting_paginations = paginator.page(paginator.num_pages)

        if "q" in request.GET:
            query = request.GET["q"]
            postings = list(Store.objects.filter(
                Q(name__icontains=query) | Q(product__title__icontains=query) | Q(product__description__icontains=query) | Q(description__icontains=query)).distinct())
            paginator = Paginator(postings, self.paginate_by)

            page = request.GET.get('page')

            try:
                posting_paginations = paginator.page(page)
            except PageNotAnInteger:
                posting_paginations = paginator.page(1)
            except EmptyPage:
                posting_paginations = paginator.page(paginator.num_pages)

            return render(request, 'businesses/index.html', {'stores': posting_paginations})

        return render(request, 'businesses/index.html', {'stores': posting_paginations})


class BusinessDetailView(DetailView):
    model = Store
    template_name = "businesses/detail.html"

    def get_context_data(self, **kwargs):
        context = {}
        store = self.get_object()
        context['store'] = store
        if self.request.user.is_authenticated:
            context['cart'] = Cart.objects.get_or_create(user=self.request.user, store=store)[0]

        return context


@csrf_exempt
def cart_add(request):
    if request.user.is_authenticated and request.is_ajax:
        product = Product.objects.get(pk=request.GET['pk'])
        cart = Cart.objects.get_or_create(user=request.user, store=product.store)[0]
        cart_product = CartProduct.objects.get_or_create(product=product, cart=cart)

        print(cart_product)

        if cart_product[1]:  # If It Was Just Created
            cart_product[0].amount = 1
            cart.products.add(cart_product[0])
        else:
            cart_product[0].amount += 1

        cart_product[0].save()

        return HttpResponse('Complete')


@csrf_exempt
def cart_remove(request):
    if request.user.is_authenticated and request.is_ajax:
        product = Product.objects.get(pk=request.GET['pk'])
        cart = Cart.objects.get_or_create(user=request.user, store=product.store)[0]
        cart_product = CartProduct.objects.get_or_create(product=product, cart=cart)

        if cart_product[1]:
            cart_product[0].delete()
        else:
            cart_product[0].amount -= 1
            cart_product[0].save()
            if cart_product[0].amount <= 0:
                cart_product[0].delete()

        return HttpResponse('Complete')


@csrf_exempt
def business_delivery(request):
    if request.is_ajax:
        value = verify_address(
            request.GET['address1'],
            request.GET['zip'],
            request.GET['city'],
            request.GET['address2']
        )

        return HttpResponse(value)

