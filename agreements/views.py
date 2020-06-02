from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView,DetailView
from .models import Agreement
from .forms import AgreementCreateForm


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
        from memberships.views import get_user_membership
        if get_user_membership(self.request).membership.membership_type == 'Free':
            return False
        return True