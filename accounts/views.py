from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,reverse
from .forms import UserRegisterForm,ProfileUpdateForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView,UpdateView,DetailView
from leases.models import House
from memberships.views import get_user_membership,get_user_subscription
from django.contrib.auth.mixins import LoginRequiredMixin


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            user = User.objects.create_user(email, password1)
            user.save()
            user = authenticate(email=email,password=password1)
            login(request, user)    
            return HttpResponseRedirect(reverse('home'))
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
        context['inactive_houses'] = House.objects.inactive_by_user(self.request.user)
        return context
