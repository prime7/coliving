from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import *
from django.shortcuts import render, redirect
from django.views.generic import FormView, DetailView, CreateView, UpdateView, ListView
from .forms import PostingCreateForm, OfferForm
from accounts.models import Notification, ChatRoom

def CategoryList(request):
    categories = Category.objects.all()
    return render(request,'buyandsell/index.html',{'categories':categories})

class CategoryDetail(ListView):
    paginate_by = 25
    model = Category

    def get(self, request, *args, **kwargs):
        category = list(Category.objects.filter(pk=self.kwargs['pk']))[0]
        postings = list(Posting.objects.filter(category=category))

        paginator = Paginator(postings, self.paginate_by)

        page = request.GET.get('page')

        try:
            posting_paginations = paginator.page(page)
        except PageNotAnInteger:
            posting_paginations = paginator.page(1)
        except EmptyPage:
            posting_paginations = paginator.page(paginator.num_pages)

        if "q" in request.GET:
            query = request.GET["q"]
            postings = list(Posting.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(city__name__icontains=query) | Q(area__name__icontains=query) | Q(
                    country__name__icontains=query) | Q(description__icontains=query)).distinct())
            paginator = Paginator(postings, self.paginate_by)

            page = request.GET.get('page')

            try:
                posting_paginations = paginator.page(page)
            except PageNotAnInteger:
                posting_paginations = paginator.page(1)
            except EmptyPage:
                posting_paginations = paginator.page(paginator.num_pages)

            return render(request, 'buyandsell/detail.html', {'postings': posting_paginations, 'category': category})

        return render(request, 'buyandsell/detail.html', {'postings': posting_paginations, 'category': category})

class PostingDetail(FormView, DetailView):
    model = Posting
    template_name = "buyandsell/posting.html"

    def get_context_data(self, **kwargs):
        context = {}
        posting = self.get_object()
        context['offer_form'] = OfferForm()
        context['posting'] = list(Posting.objects.filter(pk=posting.pk))[0]
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        posting = self.get_object()
        context['offer_form'] = OfferForm()
        context['posting'] = list(Posting.objects.filter(pk=posting.pk))[0]
        return render(request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()

        offer_form = OfferForm(request.POST)
        if offer_form.is_valid():
            offer_form = offer_form.save(commit=False)
            offer_form.posting = self.get_object()
            offer_form.applicant = request.user
            offer_form.save()
            self.object.applications.add(offer_form)

        messages.success(request, 'You have been entered as an applicant!')
        return self.render_to_response(context=context)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class PostingApplicationView(DetailView):
    model = Posting
    template_name = 'buyandsell/buyandsell_applications.html'

    def get_context_data(self,**kwargs):
        context = {}
        posting = Posting.objects.get(pk=self.object.pk)
        context['applications'] = posting.applications.all()
        context['posting'] = self.object
        return context

def ApplicationAcceptView(request, postingpk, offerpk):

    if request.user:
        posting = list(Posting.objects.filter(pk=postingpk))[0]
        offer = list(Offer.objects.filter(posting=posting, pk=offerpk))[-1]
        offer.accepted = True
        offer.save()
        posting.delete()
        messages.success(request, 'Application Accepted!')
        chatroom = ChatRoom.objects.create(topic=f"{posting.title} (${offer.offering_price})")
        chatroom.users.add(request.user, offer.applicant)
        Notification.objects.create(
            user=request.user,
            title=f"You have been added to a chatroom with {offer.applicant.username}",
            text=f"Since you have accepted {offer.applicant.username}'s offer on your posting of {posting.title}, you have been added to a chatroom with them to coordinate shipping, recieving, and/or pickup of the product."
        )
        Notification.objects.create(
            user=offer.applicant,
            title=f"Your offer for {posting.title} has been accepted!",
            text=f"Since your offer has been accepted by {request.user}, you have been added to a chatroom with them to coordinate shipping, recieving, and/or pickup of the product."
        )
        offer.applicant.email_user(
            subject=f"Your offer for {posting.title} has been accepted!",
            message=f"{request.user} has accepted your offer of ${offer.offering_price} for their posting! Head to https://meetquoteshack.com/user/chatrooms to coordinate the rental process with them!",
        )

    return redirect('user-lease')

@method_decorator(login_required(login_url='/login'), name='dispatch')
class PostingCreateView(LoginRequiredMixin, CreateView):
    model = Posting
    form_class = PostingCreateForm
    template_name = "buyandsell/create_posting.html"
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.user = self.request.user
        obj = form.save()
        obj.short_term = True
        obj.save()

        files = self.request.FILES.getlist('images')
        for f in files:
            PostingImage.objects.create(posting=obj,image=f)
        return super().form_valid(form)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class PostingDeactivateView(DetailView):
    model = Posting
    template_name = "buyandsell/deactivate_posting.html"

    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        context = context = super(PostingDeactivateView, self).get_context_data(**kwargs)

        self.object.delete()

        return redirect("user-lease")

class PostingUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Posting
    form_class = PostingCreateForm
    template_name = "buyandsell/update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        posting = self.get_object()
        if self.request.user == posting.user:
            return True
        return False
