from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import House,User,Image,Lead
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import HouseCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect


class LeaseListView(ListView):
    model = House
    template_name = "listing.html"
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
    template_name = "listing-detail.html"

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
        # TODO: Send email about the lister
        return self.render_to_response(context=context)

class UserLeaseListView(ListView):
    model = House
    template_name = 'listing-user.html'
    context_object_name = 'houses'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return House.objects.filter(user=user).order_by('-earliest_move_in')
    


@method_decorator(login_required(login_url='/login'), name='dispatch')
class LeaseCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = House
    form_class = HouseCreateForm
    template_name = "listing-create.html"
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
        return render(self.request,"upgrade-membership.html")
    