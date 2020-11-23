from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .models import *
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, CreateView
from .forms import BookingForm, ListingCreateForm

def CategoryList(request):
    categories = Category.objects.all()
    return render(request,'rentanything/index.html',{'categories':categories})

def CategoryDetail(request, pk):
    category = list(Category.objects.filter(pk=pk))[0]
    listings = list(Listing.objects.filter(category=category))
    return render(request, 'rentanything/detail.html', {'listings': listings, 'category': category})

class ListingDetail(FormView, DetailView):
    model = Listing
    template_name = "rentanything/listing.html"

    def get_context_data(self, **kwargs):
        context = {}
        listing = self.get_object()
        if self.request.user.is_authenticated:
            context['booking_form'] = BookingForm()
            context['listing'] = list(Listing.objects.filter(pk=listing.pk))[0]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        listing = self.get_object()
        if self.request.user.is_authenticated:
            context['booking_form'] = BookingForm()
            context['listing'] = list(Listing.objects.filter(pk=listing.pk))[0]
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.applications.add(request.user)
        context = self.get_context_data()

        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking_form = booking_form.save(commit=False)
            booking_form.listing = self.get_object()
            booking_form.rentee = request.user
            booking_form.save()

        messages.success(request, 'You have been entered as an applicant!')
        return self.render_to_response(context=context)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class ListingApplicationView(DetailView):
    model = Listing
    template_name = 'rentanything/rentanything_applications.html'

    def get_context_data(self,**kwargs):
        context = {}
        listing = Listing.objects.get(pk=self.object.pk)
        context['applications'] = listing.applications.all()
        context['listing'] = self.object
        booking = list(Booking.objects.filter(listing=self.object, rentee=self.request.user))
        if len(booking) > 0:
            context['booking'] = booking[-1]
        return context

def ApplicationAcceptView(request, pk):

    if request.user:
        listing = list(Listing.objects.filter(pk=pk))[0]
        booking = list(Booking.objects.filter(listing=listing))[-1]
        booking.accepted = True
        listing.applications.remove(booking.rentee)
        booking.save()
        messages.success(request, 'Application accepted!')

    return redirect('rentanything-listing', pk=pk)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = "rentanything/create_posting.html"
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()
        obj.short_term = True
        obj.save()

        files = self.request.FILES.getlist('images')
        for f in files:
            ListingImage.objects.create(listing=obj,image=f)
        return super().form_valid(form)

