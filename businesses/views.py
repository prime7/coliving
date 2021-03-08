from datetime import datetime, timedelta

from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView

from deliveranything.models import AnonymousDelivery
from .models import Store, Product, Cart, CartProduct
from .forms import AnonymousCartForm
from config.functions import verify_address
import geopy.distance
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
        elif "email" in self.request.GET:
            queryset = Cart.objects.filter(email=self.request.GET['email'], store=store)
            if len(queryset) > 0:
                context['cart'] = queryset.first()

        else:
            context['a_form'] = AnonymousCartForm()

        return context

    def post(self, request, *args, **kwargs):
        form = AnonymousCartForm(request.POST)
        return_url = request.POST.get('next', '/')

        if form.is_valid():
            cart = Cart.objects.get_or_create(email=form.cleaned_data['email'], store=self.get_object())
            if cart[1]:
                messages.success(request, "Session Successfully Created!")
            else:
                messages.success(request, "Previous Session Restored!")

            return HttpResponseRedirect(return_url + f"?email={form.cleaned_data['email']}")

        else:
            messages.warning(request, "Unexpected error. Please try again.")
            return HttpResponseRedirect(return_url)


@csrf_exempt
def payment_method(request):
    context = {}
    if request.is_ajax:
        errors = []
        if request.POST["name"] and request.POST["number"] and request.POST["cvc"] and request.POST["expiry"] and request.POST["quote"] and request.POST["address"]:
            try:
                expiry = request.POST["expiry"].split("/")
                user_card = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        "number": request.POST["number"],
                        "exp_month": int(expiry[0].strip()),
                        "exp_year": int(expiry[1].strip()),
                        "cvc": request.POST["cvc"]
                    }
                )

                if request.POST["coupon"]:
                    list = stripe.PromotionCode.list(code=request.POST['coupon'])['data']
                    if len(list) > 0:
                        off = list[0]["coupon"]["percent_off"]
                        price = float(request.POST['quote'])
                        discount = price * float(off) / 100
                        price = float(request.POST['quote']) - float(discount)
                        context["discount"] = f"Discount of ${discount} off used!"
                    else:
                        price = float(request.POST['quote'])
                else:
                    price = float(request.POST['quote'])

                charge = stripe.PaymentIntent.create(
                    amount=int(float(price) * 100),
                    currency="cad",
                    payment_method=user_card,
                    confirm=True
                )

                description = "Order"
                cart = Cart.objects.get(pk=int(request.POST['cartID']))
                for product in cart.products.all():
                    description += f"\n{product.amount}x {product.product.title} - ${product.get_cost}"

                description += f"\n\nTotal: ${cart.get_cost}"

                delivery = AnonymousDelivery.objects.create(
                    user=cart.email,
                    pickup=cart.store.business.address,
                    dropoff=request.POST["address"],
                    time=datetime.now() + timedelta(hours=4),
                    wait_time="10",
                    description=description,
                    quote=float(request.POST['quote'])
                )

                subject = 'New Delivery Order'
                message = "A new order has been created.\n"
                message += description

                cart.store.business.user.email_user(subject, message, fail_silently=False)

                context["card"] = user_card
            except stripe.error.CardError as e:
                errors.append("Card type not supported or incorrect details.")

                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                errors.append("You have sent too many requests too quickly. Try again later.")
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e.user_message)
                errors.append("An unexpected error occured. Try again.")
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                print(e.user_message)
                errors.append("An unexpected error occured. Try again.")
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                print(e.user_message)
                errors.append("A network error occured. Try again.")
            except stripe.error.StripeError as e:
                # Display a very generic error to the user
                errors.append("An unexpected error occured. Try again.")
                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)

            except Exception as e:
                # Something else happened, completely unrelated to Stripe

                errors.append("An unexpected error occured. Try again.")

                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)

        else:
            if not request.POST["quote"]:
                errors.append("Unexpected Error.")
            else:
                errors.append("Please fill all the fields.")

        context["errors"] = errors
        return JsonResponse(context)


@csrf_exempt
def cart_add(request):
    if request.user.is_authenticated and request.is_ajax:
        product = Product.objects.get(pk=request.GET['pk'])
        cart = Cart.objects.get_or_create(user=request.user, store=product.store)[0]
        cart_product = CartProduct.objects.get_or_create(product=product, cart=cart)

        if cart_product[1]:  # If It Was Just Created
            cart_product[0].amount = 1
            cart.products.add(cart_product[0])
        else:
            cart_product[0].amount += 1

        cart_product[0].save()

        return HttpResponse('Complete')
    elif request.is_ajax:
        product = Product.objects.get(pk=request.GET['pk'])
        cart = Cart.objects.get(pk=request.GET['cartID'])
        cart_product = CartProduct.objects.get_or_create(product=product, cart=cart)

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
    elif request.is_ajax:
        product = Product.objects.get(pk=request.GET['pk'])
        cart = Cart.objects.get(pk=request.GET['cartID'])
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

        return HttpResponse(value["success"])

@csrf_exempt
def retail_quote(request):
    if request.is_ajax:
        dropoff = verify_address(
            request.GET['address1'],
            request.GET['zip'],
            request.GET['city'],
            request.GET['address2']
        )

        cart = Cart.objects.get(pk=int(request.GET['cartID']))
        store = Store.objects.get(pk=int(request.GET['storeID']))

        pickup = verify_address(
            store.business.address.street_address,
            store.business.address.postal_code,
            store.business.address.business_city,
            store.business.address.apartment_address
        )

        coords_1 = (pickup["details"]["latitude"],
                    pickup["details"]["longitude"])
        coords_2 = (dropoff["details"]["latitude"],
                    dropoff["details"]["longitude"])

        distance = geopy.distance.distance(coords_1, coords_2).km

        c_price = cart.get_cost

        d_price = round(distance * 1.7, 2)

        quote = round(float(c_price) + d_price, 2)

        return HttpResponse(quote)
