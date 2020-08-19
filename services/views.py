from django.shortcuts import render
from django.views.generic import DetailView,FormView
from django.contrib import messages
from .models import Service
from .forms import TaskCreationForm


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