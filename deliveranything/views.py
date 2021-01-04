from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.forms import UserRegisterForm
from accounts.tokens import account_activation_token
from deliveranything.forms import BusinessCreationForm, AddressForm
from .forms import DeliveryForm, VehicleForm
from .models import DeliveryImage
import datetime

def index(request):

    context = {
        'deliveryform': DeliveryForm(),
        'vehicleform': VehicleForm()
    }

    if request.method == 'POST':
        deliverform = DeliveryForm(request.POST, request.FILES)

        if deliverform.is_valid():
            delivery = deliverform.save(commit=False)
            if request.user.profile.is_business:
                delivery.pickup = request.user.business.address.get_address

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

            messages.success(request, "Your delivery request has been receive. You will receive a quote shortly")
            return render(request, 'deliveranything/index.html', context)


    return render(request, 'deliveranything/index.html', context)


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

            a_form = a_form.save(commit=False)
            a_form.business = b_form
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
