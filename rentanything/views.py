from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from accounts.models import ChatRoom, Notification
from .models import *
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, CreateView, UpdateView, ListView
from .forms import BookingForm, ListingCreateForm

def CategoryList(request):
    categories = Category.objects.all()
    return render(request,'rentanything/index.html',{'categories':categories})

class CategoryDetail(ListView):
    paginate_by = 25
    model = Category

    def get(self, request, *args, **kwargs):
        category = list(Category.objects.filter(pk=self.kwargs['pk']))[0]
        listings = list(Listing.objects.filter(category=category))

        paginator = Paginator(listings, self.paginate_by)

        page = request.GET.get('page')

        try:
            listing_paginations = paginator.page(page)
        except PageNotAnInteger:
            listing_paginations = paginator.page(1)
        except EmptyPage:
            listing_paginations = paginator.page(paginator.num_pages)
        if "q" in request.GET:
            query = request.GET["q"]
            listings = list(Listing.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(city__name__icontains=query) | Q(area__name__icontains=query) | Q(
                    country__name__icontains=query)).distinct())
            paginator = Paginator(listings, self.paginate_by)

            page = request.GET.get('page')

            try:
                listing_paginations = paginator.page(page)
            except PageNotAnInteger:
                listing_paginations = paginator.page(1)
            except EmptyPage:
                listing_paginations = paginator.page(paginator.num_pages)

            return render(request, 'rentanything/detail.html', {'listings': listing_paginations, 'category': category})

        return render(request, 'rentanything/detail.html', {'listings': listing_paginations, 'category': category})

class ListingDetail(FormView, DetailView):
    model = Listing
    template_name = "rentanything/listing.html"

    def get_context_data(self, **kwargs):
        context = {}
        listing = self.get_object()
        context['booking_form'] = BookingForm()
        context['listing'] = list(Listing.objects.filter(pk=listing.pk))[0]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        listing = self.get_object()
        context['booking_form'] = BookingForm()
        context['listing'] = list(Listing.objects.filter(pk=listing.pk))[0]
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking_form = booking_form.save(commit=False)
            booking_form.listing = self.get_object()
            booking_form.rentee = request.user
            booking_form.save()
            self.object.applications.add(booking_form)

        messages.success(request, 'You have been entered as an applicant!')
        return self.render_to_response(context=context)

def ApplicationAcceptView(request, listingpk, bookingpk):

    if request.user:
        listing = list(Listing.objects.filter(pk=listingpk))[0]
        booking = list(Booking.objects.filter(listing=listing, pk=bookingpk))[-1]
        booking.accepted = True
        listing.applications.remove(booking)
        booking.save()
        messages.success(request, 'Application Accepted!')
        chatroom = ChatRoom.objects.create(topic=f"{listing.title} ({booking.start} - {booking.end})")
        chatroom.users.add(request.user, booking.rentee)
        Notification.objects.create(
            user=request.user,
            title=f"You have been added to a chatroom with {booking.rentee.username}",
            text=f"Since you have accepted {booking.rentee.username}'s booking request on your posting of {listing.title}, you have been added to a chatroom with them to coordinate shipping, receiving, and/or pickup of the product."
        )
        Notification.objects.create(
            user=booking.rentee,
            title=f"Your offer for {listing.title} has been accepted!",
            text=f"Since your booking request has been accepted by {request.user}, you have been added to a chatroom with them to coordinate shipping, receiving, and/or pickup of the product."
        )
        booking.rentee.email_user(
            subject=f"Your booking request for {listing.title} has been accepted!",
            message=f"{request.user} has accepted your booking request! Head to https://incuman.com/dashboard/chats/ to coordinate the rental process with them!",
        )

    return redirect('rentanything-listing', pk=listingpk)

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

@method_decorator(login_required(login_url='/login'), name='dispatch')
class ListingDeactivateView(DetailView):
    model = Listing
    template_name = "rentanything/deactivate_listing.html"

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = context = super(ListingDeactivateView, self).get_context_data(**kwargs)

        self.object.delete()

        return redirect("user-lease")

class ListingUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Listing
    form_class = ListingCreateForm
    template_name = "rentanything/update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        listing = self.get_object()
        if self.request.user == listing.user:
            return True
        return False
