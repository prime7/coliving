from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView,DetailView,ListView
from .models import Agreement
from .forms import AgreementCreateForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from accounts.models import User


class AgreementCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView):
    model = Agreement
    form_class = AgreementCreateForm
    template_name = "agreements/agreement-create.html"
    context_object_name = "form"

    def form_valid(self, form):
        form.instance.landlord = self.request.user
        return super().form_valid(form)

    def test_func(self):
        from memberships.views import get_user_membership
        if get_user_membership(self.request).membership.membership_type == 'Free':
            return False
        return True

class AgreementDetailView(LoginRequiredMixin,UserPassesTestMixin,DetailView):
    model = Agreement
    template_name = "agreements/agreement-detail.html"


    def test_func(self):
        obj = self.get_object()
        if obj.landlord != self.request.user:
            return False
        from memberships.views import get_user_membership
        if get_user_membership(self.request).membership.membership_type == 'Free':
            return False
        return True
    

    def handle_no_permission(self):
        return redirect('home')

    
class AgreementListView(ListView):
    model = Agreement
    template_name = 'users/agreements.html'
    context_object_name = 'agreements'
    paginate_by = 5

    def get_queryset(self):
        landlord = self.request.user
        return Agreement.objects.filter(landlord=landlord).order_by('-agreement_created')


class AgreementSignView(UserPassesTestMixin,DetailView):
    model = Agreement
    template_name = "agreements/agreement-sign.html"

    def test_func(self):
        return True