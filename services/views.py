from django.shortcuts import render,redirect,reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.tokens import account_activation_token
from django.views.generic import DetailView,FormView
from django.contrib import messages
from .models import Service
from accounts.forms import UserRegisterForm
from .forms import TaskCreationForm,TaskerCreationForm


def services(request):
    services = Service.objects.all()
    return render(request,'services/index.html',{'services':services})


class ServiceDetail(FormView,DetailView):
    model = Service 
    template_name = 'services/detail.html'
    form_class = TaskCreationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        context['services'] = Service.objects.exclude(pk=service.pk).order_by('?')[:3]
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = context = super(ServiceDetail, self).get_context_data(**kwargs)

        form = TaskCreationForm(request.POST)
        if form.is_valid():
            messages.info(request, 'We received your application, we will contact you ASAP.')
            form.save()
        else:
            messages.warning(request,'Something error happended')

        return self.render_to_response(context=context)


def signupTasker(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        t_form = TaskerCreationForm(request.POST,request.FILES)

        if u_form.is_valid() and t_form.is_valid():
            user = u_form.save(commit=False)
            user.is_active = False
            user.save()

            t_form = t_form.save(commit=False)
            t_form.user = user
            t_form.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message,fail_silently=False)
            messages.success(request, f'Your account has been updated!')
            return redirect('account_activation_sent')
    
    u_form = UserRegisterForm()
    t_form = TaskerCreationForm()
    
    context = {
        'u_form': u_form,
        't_form': t_form
    }
    return render(request, 'users/tasker_signup.html', context)