from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import House,User,Image
from django.db.models import Q,F
from django.contrib.auth.decorators import login_required
from .forms import HouseCreateForm
from django.contrib import messages
from django.shortcuts import render, redirect


class RentalListView(ListView):
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

class RentalDetailView(DetailView):
    model = House
    template_name = "listing-detail.html"
    context_object_name = "house"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        houses = House.objects.all()

        context.update({
            'houses' : houses ,
        })
        return context

# class RentalCreateView(LoginRequiredMixin, CreateView):
#     model = House
#     form_class = HouseCreateForm
#     template_name = 'listing-create.html'

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)


class UserRentalListView(ListView):
    model = House
    template_name = 'listing-user.html'
    context_object_name = 'houses'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return House.objects.filter(user=user).order_by('-earliest_move_in')
    
class RentalCreateView(LoginRequiredMixin, CreateView):
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
    