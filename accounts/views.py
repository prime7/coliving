import easypost
from django.contrib.messages.views          import SuccessMessageMixin
from django.contrib.auth                    import login
from django.shortcuts                       import render, redirect,reverse

from businesses.models import Store, Product
from deliveranything.forms import AddressForm
from businesses.forms import StoreForm, ProductForm
from .forms                                 import UserRegisterForm, ProfileUpdateForm, ProfileVerificationForm, ContactForm, ListingDataListForm, LookingDataListForm
from .models                                import User, NewsLetter, ListingDataList, Profile, LookingDataList
from rentanything.models                    import Listing
from buyandsell.models                      import Posting
from django.conf                            import settings
from django.contrib.auth.decorators         import login_required
from django.contrib                         import messages
from django.views.generic                   import ListView, CreateView
from django.db.models                       import Q
from rentals.models                         import House
from memberships.views                      import get_user_membership,get_user_subscription
from django.contrib.auth.mixins             import LoginRequiredMixin
from .tokens                                import account_activation_token
from django.contrib.sites.shortcuts         import get_current_site
from django.utils.encoding                  import force_bytes
from django.utils.http                      import urlsafe_base64_encode
from django.template.loader                 import render_to_string
from django.utils.encoding                  import force_text
from django.utils.http                      import urlsafe_base64_decode
from django.shortcuts                       import render_to_response
from django.template                        import RequestContext
from services.models                        import Service
from accounts.models                        import Notification, Landlord
from memberships.models                     import Membership
from itertools                              import chain
from deliveranything.models                 import Address, Business
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    services = Service.objects.all()
    memberships = Membership.objects.all()
    service_list = []
    if 0 < len(services) < 9:
        for i in range(len(services)):
            service_list.append(services[i])
    elif len(services) >= 9:
        for i in range(9):
            service_list.append(services[i])

    query = request.GET.get('q')
    if query:
        rentanything = Listing.objects.filter(Q(title__icontains=query) |
                                              Q(description__icontains=query) |
                                              Q(city__name__icontains=query) |
                                              Q(area__name__icontains=query) |
                                              Q(country__name__icontains=query)
                                              ).distinct()
        buyandsell = Posting.objects.filter(Q(title__icontains=query) |
                                            Q(description__icontains=query) |
                                            Q(city__name__icontains=query) |
                                            Q(area__name__icontains=query) |
                                            Q(country__name__icontains=query)
                                            ).distinct()
        listing = House.objects.filter(Q(title__icontains=query) |
                                       Q(description__icontains=query) |
                                       Q(city__icontains=query)
                                       ).distinct().order_by('-earliest_move_in')

        results = list(chain(rentanything, listing, buyandsell))

        if len(results) > 0:
            return render(request, 'accounts/query.html', {'results': results[:25], 'query': query})
        else:
            messages.warning(request, "No Matching Requests Found.")


    return render(request,'accounts/home.html',{'services':service_list, 'memberships':memberships})

# START TEMPORARY VIEW
class ListingDataListCreateView(SuccessMessageMixin, CreateView):
    model = ListingDataList
    success_message = 'Thank you for your response!'
    form_class = ListingDataListForm

    def get_success_url(self):
        self.object.phone = self.object.get_phone_number
        self.object.price = self.object.get_price_range
        self.object.save()

        if self.request.META.get('HTTP_REFERER'):
            return self.request.META.get('HTTP_REFERER')
        else:
            return reverse('home')

class LookingDataListCreateView(SuccessMessageMixin, CreateView):
    model = LookingDataList
    success_message = 'Thank you for your response!'
    form_class = LookingDataListForm

    def get_success_url(self):
        self.object.phone = self.object.get_phone_number
        self.object.save()

        if self.request.META.get('HTTP_REFERER'):
            return self.request.META.get('HTTP_REFERER')
        else:
            return reverse('home')
# END TEMPORARY VIEW

def signup(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # Referral Code Usage
            if form.cleaned_data['code']:
                referrer = Profile.objects.filter(referral_code=form.cleaned_data['code']).first()
                if referrer:
                    referrer.referred_users.add(user)

            current_site = get_current_site(request)
            subject = 'Welcome to incuman <3 Activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,fail_silently=False)
            return redirect('account_activation_sent')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def userDetail(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('user-detail')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        business = Business.objects.filter(user=request.user).first()
        address = Address.objects.filter(business=business).first()
        if address:
            a_form = AddressForm(instance=request.user.business.address)
        else:
            a_form = AddressForm()

    context = {
        'p_form': p_form,
        'a_form': a_form,
    }

    return render(request, 'users/detail.html', context)


@login_required
def userBusiness(request):
    business = Business.objects.get(user=request.user)
    store = Store.objects.filter(business=business).first()

    if store:
        s_form = StoreForm(instance=business.store)
    else:
        s_form = StoreForm()

    context = {
        'business': business,
        's_form': s_form,
        'p_form': ProductForm()
    }

    return render(request, 'users/business.html', context)


@login_required
def productDelete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    messages.success(request, 'Product Deleted!')

    return redirect('user-business')


@login_required
def productForm(request):
    if request.method == 'POST':
        business = Business.objects.get(user=request.user)
        store = Store.objects.filter(business=business).first()

        p_form = ProductForm(request.POST, request.FILES)
        if p_form.is_valid():
            messages.success(request, 'Your store has been updated!')
            p_form = p_form.save(commit=False)
            p_form.store = store
            p_form.save()

        return redirect('user-business')

@login_required
def storeForm(request):
    if request.method == 'POST':
        business = Business.objects.get(user=request.user)
        store = Store.objects.filter(business=business).first()
        if store:
            s_form = StoreForm(request.POST, instance=request.user.business.store)
        else:
            s_form = StoreForm(request.POST)
        if s_form.is_valid():
            messages.success(request, 'Your store has been updated!')
            s_form = s_form.save(commit=False)
            s_form.business = request.user.business
            s_form.save()

            return redirect('user-business')


@login_required
def addressForm(request):
    if request.method == 'POST':
        a_form = AddressForm(request.POST, instance=request.user.business.address)
        if a_form.is_valid():
            messages.success(request, 'Your address has been updated!')
            address = easypost.Address.create(
                verify=["delivery"],
                street1=a_form.cleaned_data['street_address'],
                street2=a_form.cleaned_data['apartment_address'],
                zip=a_form.cleaned_data['postal_code'],
                city=a_form.cleaned_data['business_city'],
                country=a_form.cleaned_data['business_country'],
            )
            a_form = a_form.save(commit=False)
            a_form.verified = address.verifications["delivery"]["success"]
            a_form.save()
            return redirect('user-detail')


    context = {
        'a_form': a_form,
    }

    return render(request, 'users/detail.html', context)


@login_required
def userPayment(request):

    context = {}

    if request.method == "POST":
        if request.POST["name"] and request.POST["number"] and request.POST["cvc"] and request.POST["expiry"]:
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
                stripe.PaymentMethod.attach(
                    user_card["id"],
                    customer=request.user.profile.customer_code
                )
            except stripe.error.CardError as e:
                messages.info(request, "Card type not supported.")

                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)
            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.info(request, "You have sent too many requests too quickly. Try again later.")
            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                messages.info(request, "An unexpected error occured. Try again.")
            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.info(request, "An unexpected error occured. Try again.")
            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.info(request, "A network error occured. Try again.")
            except stripe.error.StripeError as e:
                # Display a very generic error to the user
                messages.info(request, "An unexpected error occured. Try again.")
                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)

            except Exception as e:
                # Something else happened, completely unrelated to Stripe

                messages.info("An unexpected error occured. Try again.")

                print('Status is: %s' % e.http_status)
                print('Code is: %s' % e.code)
                # param is '' in this case
                print('Param is: %s' % e.param)
                print('Message is: %s' % e.user_message)

        else:
            messages.info(request, "Please fill all the fields.")

    methods = stripe.PaymentMethod.list(
        customer=request.user.profile.customer_code,
        type="card"
    )
    context["methods"] = methods

    return render(request, "users/payments.html", context)


@login_required
def removeCard(request, id):
    stripe.PaymentMethod.detach(
        id
    )
    messages.success(request, "Card Removed.")

    return redirect('user-payment')


@login_required
def userVerification(request):
    if request.method == 'POST':
        p_form = ProfileVerificationForm(request.POST,request.FILES,instance=request.user.profile)
        if p_form.is_valid():
            p_form = p_form.save(commit=False)
            p_form.verified = 2
            p_form.save()
            messages.success(request, 'Your verification document is been succesfully updated')
        return redirect('user-verification')
    else:
        p_form = ProfileVerificationForm()
    context = {
        'p_form': p_form
    }
    return render(request, 'users/verification.html',context)

@login_required
def notificationDelete(request, pk):

    notification = list(Notification.objects.all().filter(pk=pk, user=request.user).order_by('-date_created'))[0]

    if request.method == "POST":
        if request.user == notification.user:

            messages.success(request, "Notification has been deleted.")

            notification.delete()

            return redirect('notifications')
        else:
            return redirect('notifications')
    else:
        return redirect('notifications')

def contact(request):
    if request.method == 'POST':
        c_form = ContactForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.success(request, 'We have received your request')
        return redirect('home')
    else:
        c_form = ContactForm()
    context = {
        'c_form': c_form
    }
    return render(request, 'accounts/contact.html',context)

@login_required
def userMembership(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, 'users/membership.html', context)


class UserLease(LoginRequiredMixin,ListView):
    model = House
    template_name = 'users/leases.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        landlord = Landlord.objects.filter(user=self.request.user)[0]
        context['active_houses'] = House.objects.active_by_landlord(landlord=landlord)
        context['inactive_houses'] = House.objects.filter(landlord=landlord,rented=True,active=True)
        context['short_houses'] = House.objects.filter(landlord=landlord,short_term=True,rented=False)
        context['rentanything'] = Listing.objects.filter(user=self.request.user)
        context['buyandsell'] = Posting.objects.filter(user=self.request.user)
        return context

def account_activation_sent(request):
    return render(request, 'accounts/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_varified = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'accounts/account_activation_invalid.html')

def page_not_found_view(request):
    response = render_to_response('404.html', {},context_instance=RequestContext(request))
    response.status_code = 404
    return response

def newsletter_signup(request):
    if request.method == 'POST':
        letters = NewsLetter.objects.filter(email=request.POST.get('newsletter'))
        if letters.count() >= 1:
            messages.error(request, 'Your email has already been registered to our News Letter.')
        else:
            newsletter = NewsLetter.create(request.POST.get('newsletter'))
            newsletter.save()
            if newsletter.id:
                messages.success(request, 'Your email has been registered for our News Letter!')
            else:
                messages.warning(request, 'Email could not be entered into News Letter at this time. Please try again.')

    return render(request, 'accounts/home.html', )


def about_us(request):
    return render(request, 'accounts/about-us.html')
