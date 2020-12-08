from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,View,FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import House,User,Image,Lead, Landlord, Tenant, SfvApplication, SfvDay
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HouseCreateForm,BookingForm,ShortHouseCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.http import HttpResponse
from accounts.forms import ProfileConnectForm
from datetime import datetime
from datetime import date



class ShortTermListingListview(ListView):
    model = House
    template_name = "rentals/listing.html"
    paginate_by = 6
    context_object_name = 'houses'
    queryset = House.objects.short_term_rentals()

    def get(self, request, *args, **kwargs):
        if request.GET:
            houses = House.objects.short_term_rentals()
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


class LeaseListView(ListView):
    model = House
    template_name = "rentals/listing.html"
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
    template_name = "rentals/listing-detail.html"
    form_class = ProfileConnectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        house = self.get_object()
        print(house.id)
        has_applied = False

        sfvapplications = self.request.user.tenant.sfvapplication_set.all()

        if sfvapplications:
            for x in sfvapplications:
                if x.listing.id == house.id:
                    has_applied = True


        if self.request.user.is_authenticated:
            context['form'] = ProfileConnectForm(instance=self.request.user.profile)
            context['booking_form'] = BookingForm()
            context['is_favourite'] = house.favourites.filter(id=self.request.user.id).exists()
            context['has_applied']  = has_applied
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        self.object.applications.add(request.user)
        context = context = super(LeaseDetailView, self).get_context_data(**kwargs)

        email = request.user.email
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking_form = booking_form.save(commit=False)
            booking_form.house = self.get_object()
            booking_form.user = request.user
            booking_form.save()

        form = ProfileConnectForm(request.POST,instance=self.request.user.profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Please check your email inbox')
            from django.conf import settings
            link = ""

            if settings.DEBUG:
                link = "http://127.0.0.1:8000"
            else:
                link = "https://www.meetquoteshack.ca"

            link += request.get_full_path()

            if not Lead.objects.filter(email=email,link=link).exists():
                Lead.objects.create(email=email,link=link)
            lister_name = context['object'].landlord.user.email
            lister_phone = context['object'].landlord.user.profile.mobile_number

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
    template_name = "rentals/listing-deactivate.html"

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
    template_name = 'rentals/listing-user.html'
    context_object_name = 'houses'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        landlord = user.landlord
        return House.objects.active_by_landlord(landlord)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['user'] = user
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
class LeaseCreateView(LoginRequiredMixin, CreateView):
    model = House
    form_class = HouseCreateForm
    template_name = "rentals/listing-create-long.html"
    context_object_name = "form"

    def form_valid(self, form):
        user = User.objects.filter(id=self.request.user.id)[0]
        form.instance.landlord = user.landlord
        obj = form.save()
        obj.short_term = False
        obj.save()

        #files = self.request.FILES.getlist('images')
        #for f in files:
        #    Image.objects.create(house=obj,src=f)
        return super().form_valid(form)



@method_decorator(login_required(login_url='/login'), name='dispatch')
class ShortLeaseCreateView(LoginRequiredMixin, CreateView):
    model = House
    form_class = ShortHouseCreateForm
    template_name = "rentals/listing-create-short.html"
    context_object_name = "form"

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        form.instance.landlord = user.landlord
        obj = form.save()
        obj.short_term = True
        obj.save()

        files = self.request.FILES.getlist('images')
        for f in files:
            Image.objects.create(house=obj,src=f)
        return super().form_valid(form)


class LeaseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = House
    form_class = HouseCreateForm
    template_name = "rentals/update.html"

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.user:
            return True
        return False


class ShortLeaseUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = House
    form_class = ShortHouseCreateForm
    template_name = "rentals/short-update.html"

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        house = self.get_object()
        if self.request.user == house.user:
            return True
        return False


#Ajax
@login_required
def sfv_application(request):
    try:
            ad_id = request.GET.get('ad_id')
            sfv_name = request.GET.get("sfv_name")
            sfv_phone = request.GET.get("sfv_phone")
            sfv_notes = request.GET.get("sfv_notes")
            sfv_avail = request.GET.get("sfv_avail")

            if not (ad_id and sfv_name and sfv_phone and sfv_notes and sfv_avail):
                return HttpResponse("error")

            listing = House.objects.filter(id=ad_id)
            print(listing)
            if listing:
                listing = listing[0]
            else:
                return HttpResponse('error')

            tenant = request.user.tenant
            landlord = listing.landlord

            sfv_application = SfvApplication.objects.filter(tenant=tenant, listing=listing)
            print(sfv_application)
            if sfv_application:
                   return HttpResponse('error')

            sfv_avail_list = sfv_avail.split(',')
            if len(sfv_avail_list) > 3:
                return HttpResponse("error")

            sfv_avail_date = []
            for x in sfv_avail_list:
                a = datetime.strptime(x, '%Y-%m-%d').date()
                sfv_avail_date.append(a)


            sfv_application = SfvApplication.objects.create(tenant=tenant, listing=listing, name=sfv_name, phone_number=sfv_phone, notes=sfv_notes)

            for y in sfv_avail_date:
                SfvDay.objects.create(sfv_application=sfv_application, date=y)

            return HttpResponse("done")
    except Exception as e:
        print(e)
        return HttpResponse("error")


        
