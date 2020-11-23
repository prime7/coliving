from django.http                            import HttpResponse,HttpResponseRedirect
from django.contrib.auth                    import login, authenticate
from django.contrib.auth.forms              import UserCreationForm
from django.shortcuts                       import render, redirect,reverse
from .forms                                 import UserRegisterForm,ProfileUpdateForm,ProfileVerificationForm,ContactForm
from .models                                import User, NewsLetter
from django.contrib.auth.decorators         import login_required
from django.contrib                         import messages
from django.views.generic                   import ListView,UpdateView,DetailView
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
from django.contrib.auth import logout
from services.models import Service

def home(request):
    services = Service.objects.all()
    return render(request,'accounts/home.html',{'services':services})


def signup(request):
    #logout(request)
    #u = User.objects.all()[0]

    #print(u)
    #login(request, u)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Welcome to Meetquoteshack <3 Activate your account'
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

    context = {
        'p_form': p_form
    }
    return render(request, 'users/detail.html', context)

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
        context['active_houses'] = House.objects.active_by_user(self.request.user)
        context['inactive_houses'] = House.objects.filter(user=self.request.user,rented=True,active=True)
        context['short_houses'] = House.objects.filter(user=self.request.user,short_term=True,rented=False)
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
