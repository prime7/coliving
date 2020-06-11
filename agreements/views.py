from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import CreateView,DetailView,ListView
from .models import Agreement
from .forms import AgreementCreateForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib import messages
from datetime import datetime

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['processing'] = Agreement.objects.processing(self.request.user)
        context['active'] = Agreement.objects.active(self.request.user)
        context['inactive'] = Agreement.objects.inactive(self.request.user)
        return context


class AgreementSignView(UserPassesTestMixin,DetailView):
    model = Agreement
    template_name = "agreements/agreement-sign.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST['agree'] == "1":
            self.object.status = 2
            self.object.signed_on = datetime.now()
            self.object.save()
            messages.success(request, 'You have successfully signed the contract')
            return redirect('home')
        return self.render_to_response(context={})

    def test_func(self):
        obj = self.get_object()
        if obj.tenants_email != self.request.user.email or obj.status != 1:
            return False
        return True

    def handle_no_permission(self):
        return redirect('home')