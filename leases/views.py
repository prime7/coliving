from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,View,FormView
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
from django.http import HttpResponse
from accounts.forms import ProfileConnectForm


class LeaseListView(ListView):
    model = House
    template_name = "leases/listing.html"
    paginate_by = 6
    context_object_name = 'houses'
    queryset = House.objects.active()
    
    def get(self, request, *args, **kwargs):
        if request.GET:
            houses = House.objects.active()
            query = request.GET["q"]
            if query=='vancouver':
                query = 1
            elif query == 'toronto':
                query = 2
            elif query == 'seattle':
                query = 3
            elif query == 'newyork':
                query = 4

            if query:
                houses = houses.filter(Q(title__icontains=query)|Q(city__icontains=query)|Q(description__icontains=query)).distinct().order_by('-earliest_move_in')
                return render(request, self.template_name, {'houses': houses})
        return super().get(request, *args, **kwargs)

class LeaseDetailView(FormView,DetailView):
    model = House
    template_name = "leases/listing-detail.html"
    form_class = ProfileConnectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        if self.request.user.is_authenticated:
            context['form'] = ProfileConnectForm(instance=self.request.user.profile)
            context['is_favourite'] = house.favourites.filter(id=self.request.user.id).exists()
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.applications.add(request.user)
        context = context = super(LeaseDetailView, self).get_context_data(**kwargs)
        messages.info(request, 'Please check your email inbox')
        email = request.user.email
        form = ProfileConnectForm(request.POST,instance=self.request.user.profile)
        if form.is_valid:
            form.save()
        phone_number = request.POST['mobile_number']
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

@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseDeactivateView(DetailView):
    model = House
    template_name = "leases/listing-deactivate.html"

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = context = super(LeaseDeactivateView, self).get_context_data(**kwargs)
        
        status = request.POST['status']
        if status == "1":
            self.object.rental_status = 1
        elif status == "2":
            self.object.rental_status = 2

        self.object.rented = True
        self.object.save()
        return redirect("user-lease")

@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseFavouriteView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id',None)
        house = get_object_or_404(House,id=id)
        if house.favourites.filter(id=request.user.id).exists():
            house.favourites.remove(request.user)
        else:
            house.favourites.add(request.user)
        
        return redirect('listing-detail', slug=house.slug)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class UserLeaseApplicationView(DetailView):
    model = House
    template_name = 'users/applications.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        house = House.objects.get(slug=slug)
        context['applications'] = house.applications.all()
        return context

class UserLeaseListView(ListView):
    model = House
    template_name = 'leases/listing-user.html'
    context_object_name = 'houses'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return House.objects.active_by_user(user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(email=self.request.user.email)
        return context

@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseFavouriteListView(ListView):
    model = House
    template_name = 'users/favourites.html'
    context_object_name = 'houses'

    def get_queryset(self):
        user = self.request.user 
        return user.favourites.all()

@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = House
    form_class = HouseCreateForm
    template_name = "leases/listing-create.html"
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()
        
        from memberships.context_processors import get_user_membership,is_landlord
        if not is_landlord(self.request):
            obj.rented = True
            obj.save()

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