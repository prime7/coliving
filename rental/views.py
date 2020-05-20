from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import House
from django.db.models import Q,F


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
    template_name = "list-detail.html"
    context_object_name = "house"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        houses = House.objects.all()

        context.update({
            'houses' : houses ,
        })
        return context