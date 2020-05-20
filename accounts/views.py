from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,reverse
from .forms import UserRegisterForm,ProfileUpdateForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request,"base.html")


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
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form': p_form
    }

    return render(request, 'profile.html', context)