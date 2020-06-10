from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import House,User,Image,Lead
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HouseCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail


class LeaseListView(ListView):
    model = House
    template_name = "leases/listing.html"
    paginate_by = 6
    context_object_name = 'houses'
    queryset = House.objects.all().order_by('-earliest_move_in')
    
    def get(self, request, *args, **kwargs):
        if request.GET:
            houses = House.objects.all()
            query = request.GET["q"]
            if query:
                houses = houses.filter(Q(title__icontains=query)|Q(description__icontains=query)).distinct().order_by('-earliest_move_in')
                return render(request, self.template_name, {'houses': houses})
        return super().get(request, *args, **kwargs)

class LeaseDetailView(DetailView):
    model = House
    template_name = "leases/listing-detail.html"

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = context = super(LeaseDetailView, self).get_context_data(**kwargs)
        messages.info(request, 'Please check your email inbox')
        
        email = request.POST['email']
        phone_number = request.POST['phone']
        from django.conf import settings
        link = ""
        if settings.DEBUG:
            link = "http://127.0.0.1:8000"
        else:    
            link = "https://www.meetquoteshack.ca"
        link += request.get_full_path()

        if not Lead.objects.filter(email=email,phone_number=phone_number,link=link).exists():
            Lead.objects.create(email=email,phone_number=phone_number,link=link)
        lister_name = context['object'].user.email
        lister_phone = context['object'].user.profile.mobile_number

        message = render_to_string('emails/connect_lister.html', {
            'email': email,
            'lister_phone': lister_phone,
            'lister_name': lister_name,
            'link': link
        })
        send_mail('Lister information for leasing',message,settings.EMAIL_HOST_USER, [email],  fail_silently=False,)

        return self.render_to_response(context=context)

class UserLeaseListView(ListView):
    model = House
    template_name = 'leases/listing-user.html'
    context_object_name = 'houses'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return House.objects.filter(user=user).order_by('-earliest_move_in')
    


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = House
    form_class = HouseCreateForm
    template_name = "leases/listing-create.html"
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()
        files = self.request.FILES.getlist('images')
        for f in files:
            Image.objects.create(house=obj,src=f)
        return super().form_valid(form)

    def test_func(self):
        from memberships.views import get_user_membership
        if get_user_membership(self.request).membership.membership_type == 'Free':
            return True
        return True

    def handle_no_permission(self):
        return render(self.request,"memberships/upgrade-membership.html")
    

class LeaseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = House
    form_class = HouseCreateForm
    template_name = "leases/update.html"
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.user:
            return True
        return False