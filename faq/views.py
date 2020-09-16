from django.shortcuts import render
from .models import Faq
from django.views.generic import ListView


class FaqListview(ListView):
    model = Faq
    template_name = "faq/index.html"
    context_object_name = "faqs"
    queryset = Faq.objects.all()