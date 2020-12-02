from django.urls import path
from finances.views.loan import LoanCreateAPIView
from finances.views.insurance import InsuranceCreateView
from django.views.generic import TemplateView


urlpatterns = [
    path('loan/', LoanCreateAPIView.as_view()),
    path('insurance/', InsuranceCreateView.as_view()),
    path('',TemplateView.as_view(template_name="finances/finance-forms.html"),name="finance-home")
]
