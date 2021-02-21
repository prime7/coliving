from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from accounts.forms import UserRegisterForm
from accounts.tokens import account_activation_token
from businesses.models import Cart
from deliveranything.forms import BusinessCreationForm, AddressForm
from .forms import DeliveryForm, VehicleForm, AnonymousDeliveryForm
from .models import DeliveryImage, AnonymousDeliveryImage, Delivery
import datetime
import json
import config.easypost as ep
import easypost
import geopy.distance
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
easypost.api_key = ep.EASYPOST_KEY

def index(request):

    context = {
        'deliveryform': DeliveryForm(),
        'vehicleform': VehicleForm()
    }

    if request.method == 'POST':
        if request.user.is_authenticated:
            deliverform = DeliveryForm(request.POST, request.FILES)

            if deliverform.is_valid():
                delivery = deliverform.save(commit=False)
                delivery.user = request.user
                t = deliverform.cleaned_data['date_time']
                d = deliverform.cleaned_data['date']
                delivery.time = datetime.datetime.combine(d, t)
                delivery.save()

                files = request.FILES.getlist('images')
                for f in files:
                    DeliveryImage.objects.create(
                        delivery=delivery,
                        image=f
                    )

                messages.success(request, "Your delivery request has been received. You will receive a quote shortly")
                return render(request, 'deliveranything/index.html', context)
            else:
                messages.info(request, "Please fill in all required fields properly.")
        else:
            deliverform = AnonymousDeliveryForm(request.POST, request.FILES)
            if deliverform.is_valid():
                delivery = deliverform.save(commit=False)
                t = deliverform.cleaned_data['date_time']
                d = deliverform.cleaned_data['date']
                delivery.time = datetime.datetime.combine(d, t)
                delivery.save()

                if delivery.phone:
                    delivery.phone = delivery.get_phone_number
                    delivery.save()

                files = request.FILES.getlist('images')
                for f in files:
                    AnonymousDeliveryImage.objects.create(
                        delivery=delivery,
                        image=f
                    )
                messages.success(request, "Your delivery request has been received. You will receive a quote in your email shortly")
            else:
                messages.info(request, "Please fill in all required fields properly.")

    if not request.user.is_authenticated:
        context['deliveryform'] = AnonymousDeliveryForm

    return render(request, 'deliveranything/index.html', context)


@csrf_exempt
def ajax_accept(request):

    if request.user.is_authenticated:

        data = request.GET.get("values")
        values = json.loads(data)
        try:
            delivery = Delivery.objects.create(
                user=request.user,
                pickup=values["pickup"],
                dropoff=values["dropoff"],
                time=datetime.datetime.combine(datetime.datetime.strptime(values["date"], '%Y-%m-%d').date(), datetime.datetime.strptime(values["date_time"], '%H:%M').time()),
                wait_time=values["wait_time"],
                description=values["description"],
                quote=float(values["quote"])
            )
            if values["width"]:
                delivery.width = int(values["width"])
            if values["length"]:
                delivery.length = int(values["length"])
            if values["height"]:
                delivery.height = int(values["height"])
            if values["weight"]:
                delivery.weight = int(values["weight"])

            delivery.save()

        except Exception as e:
            return HttpResponse("Delivery Not Created")

        return HttpResponse(delivery.pk)
    else:
        deliverform = AnonymousDeliveryForm(request.POST, request.FILES)
        if deliverform.is_valid():
            delivery = deliverform.save(commit=False)
            t = deliverform.cleaned_data['date_time']
            d = deliverform.cleaned_data['date']
            delivery.time = datetime.datetime.combine(d, t)
            delivery.save()

            files = request.FILES.getlist('images')
            for f in files:
                AnonymousDeliveryImage.objects.create(
                    delivery=delivery,
                    image=f
                )
            return HttpResponse("Your delivery request has been received. You will receive a quote in your email shortly")
        else:
            return HttpResponse("Please fill in all required fields properly.")


@login_required
def registerVehicle(request):

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.driver = request.user.tasker
            vehicle.save()
            messages.success(request, f"Your {vehicle.year} {vehicle.make} {vehicle.model} has been registered.")

    return redirect('deliver-anything')


def signupBusiness(request):

    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        b_form = BusinessCreationForm(request.POST,request.FILES)
        a_form = AddressForm(request.POST)

        if u_form.is_valid() and b_form.is_valid() and a_form.is_valid():
            user = u_form.save(commit=False)
            user.is_active = False
            user.save()

            b_form = b_form.save(commit=False)
            b_form.user = user
            b_form.save()

            address = easypost.Address.create(
                verify=["delivery"],
                street1=a_form.cleaned_data['street_address'],
                street2=a_form.cleaned_data['apartment_address'],
                zip=a_form.cleaned_data['postal_code'],
                city=a_form.cleaned_data['business_city'],
                country=a_form.cleaned_data['business_country'],
            )

            a_form = a_form.save(commit=False)
            a_form.business = b_form
            a_form.verified = address.verifications["delivery"]["success"]
            a_form.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,fail_silently=False)
            messages.warning(request, f'You Must Confirm Email To Log In!')
            return redirect('account_activation_sent')

    u_form = UserRegisterForm()
    b_form = BusinessCreationForm()
    a_form = AddressForm()

    context = {
        'u_form': u_form,
        'b_form': b_form,
        'a_form': a_form,
    }
    return render(request, 'users/business_signup.html', context)


@csrf_exempt
def get_methods(request):
    methods = stripe.PaymentMethod.list(customer=request.user.profile.customer_code, type="card")

    if int(len(methods["data"])) > 0:
        return JsonResponse(methods)
    else:
        return HttpResponse("You don't have a saved payment method. Please add one in your account details before continuing.")


@login_required
def payment(request):
    if request.GET.get('card') and request.GET.get('quote') and request.GET.get('id'):
        delivery = Delivery.objects.get(pk=int(request.GET.get('id')))
        card = stripe.PaymentMethod.retrieve(request.GET.get('card'))
        intent = stripe.PaymentIntent.create(
            amount=int(float(request.GET.get('quote')) * 100),
            customer=request.user.profile.customer_code,
            currency="cad",
            payment_method=card,
        )
        delivery.intent = intent["id"]
        delivery.save()

        messages.success(request, "Pre-Authorization made. A charge will be made when the delivery is made.")
        return redirect('deliver-anything')
    elif request.GET.get('card') and request.GET.get('quote') and request.GET.get('pickup') and request.GET.get('dropoff') and request.GET.get('cartID'):
        description = "Order"
        cart = Cart.objects.get(pk=int(request.GET.get('cartID')))
        for product in cart.products.all():
            description += f"\n{product.amount}x {product.product.title} - ${product.get_cost}"

        if request.GET.get('coupon'):
            list = stripe.PromotionCode.list(code=request.GET.get('coupon'))['data']
            if len(list) > 0:
                off = list[0]["coupon"]["percent_off"]
                price = float(request.GET.get('quote'))
                discount = price * float(off) / 100
                price = float(request.GET.get('quote')) - float(discount)
            else:
                price = float(request.GET.get('quote'))
        else:
            price = float(request.GET.get('quote'))

        description += f"\n\nTotal: ${cart.get_cost}"

        delivery = Delivery.objects.create(
            user=request.user,
            pickup=request.GET.get('pickup'),
            dropoff=request.GET.get('dropoff'),
            time=datetime.datetime.now() + timedelta(hours=4),
            wait_time="10",
            description=description,
            quote=price
        )

        card = stripe.PaymentMethod.retrieve(request.GET.get('card'))

        intent = stripe.PaymentIntent.create(
            amount=int(float(price) * 100),
            customer=request.user.profile.customer_code,
            currency="cad",
            payment_method=card,
        )
        delivery.intent = intent["id"]
        delivery.save()

        subject = 'New Delivery Order'
        message = "A new order has been created.\n"
        message += description

        cart.store.business.user.email_user(subject, message, fail_silently=False)
        if request.GET.get('coupon'):
            messages.success(request, f"Promo code used for ${discount} off!")
        else:
            messages.success(request, "Pre-Authorization made. A charge will be made when the delivery is made.")
        cart.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


    messages.error(request, "An unexpected error occured. Please try again.")
    return redirect('deliver-anything')


@csrf_exempt
def quote_ajax(request):
    if request.is_ajax():
        response = {}
        if not request.user.is_authenticated:
            # Manual
            response["error"] = "Since you do not have an account, we will need to manually calculate the price of delivery.<br> <span class='text-success'>(Note: This process will take longer)</span>"
            return HttpResponse(json.dumps(response))

        values = request.GET.get('values')
        data = json.loads(values)
        if data['pickup'] and data['dropoff']:
            if data['wait_time']:
                dropoff = easypost.Address.create(verify=["delivery"], street1=data['dropoff'], country="Canada")
                response["dropoff"] = dropoff.verifications["delivery"]["success"]
                if request.user.is_authenticated and request.user.profile.is_business:
                    divisor = 166
                else:
                    divisor = 139

                pickup = easypost.Address.create(verify=["delivery"], street1=data['pickup'], country="Canada")
                response["pickup"] = pickup.verifications["delivery"]["success"]

                if response["dropoff"] and response["pickup"]:

                    coords_1 = (pickup.verifications["delivery"]["details"]["latitude"], pickup.verifications["delivery"]["details"]["longitude"])
                    coords_2 = (dropoff.verifications["delivery"]["details"]["latitude"], dropoff.verifications["delivery"]["details"]["longitude"])

                    distance = geopy.distance.distance(coords_1, coords_2).km

                    d_price = round(distance * 1.7, 2)

                    if data['length'] and data['width'] and data['height']:

                        dim = round((int(data['length']) * int(data['width']) * int(data['height'])) / divisor, 2)
                        response["DIM"] = dim

                        if data["weight"]:
                            if 0 < int(data["weight"]) and 66 >= int(data["weight"]):
                                if int(data["weight"]) > dim:
                                    quote = 55
                                else:
                                    quote = round(dim * 0.85, 2)
                            else:
                                quote = round(dim * 0.85, 2)
                        else:
                            quote = round(dim * 0.85, 2)


                        response["quote"] = round(quote + d_price, 2)

                        response_data = json.dumps(response)
                        return HttpResponse(response_data)

                    elif data["weight"]:
                        if 0 < int(data["weight"]) and 66 >= int(data["weight"]):
                            quote = 56
                            response["quote"] = round(quote + d_price, 2)
                            response_data = json.dumps(response)
                            return HttpResponse(response_data)
                        else:
                            response["error"] = "Weight can be a maximum of 66 pounds."
                            return HttpResponse(json.dumps(response))

                    else:
                        # Manual
                        response["error"] = "Since you have not provided DIM dimensions and/or weight, we will need to manually calculate the price of delivery.<br> <span class='text-success'>(Note: This process will take longer)</span>"
                        return HttpResponse(json.dumps(response))

                else:
                    if not response["dropoff"] and response["pickup"]:
                        response["error"] = "Dropoff Location is not valid. Please try to enter it again."
                        return HttpResponse(json.dumps(response))
                    elif response["dropoff"] and not response["pickup"]:
                        response["error"] = "Pickup Location is not valid. Please try to enter it again."
                        return HttpResponse(json.dumps(response))

                    else:
                        response["error"] = "Pickup & Dropoff Locations is not valid. Please try to enter it again."
                        return HttpResponse(json.dumps(response))

            else:
                response["error"] = "Wait Time not provided. Please select how long the driver will have to wait to recieve the delivery."
                return HttpResponse(json.dumps(response))

        else:
            response["error"] = "Missing Pickup and Dropoff"
            return HttpResponse(json.dumps(response))

    return HttpResponse("Error")

