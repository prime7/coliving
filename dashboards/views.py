from django.shortcuts import render
from .forms import CurrentDashForm


# Create your views here.
def dashboard(request):
    user            = request.user
    is_tasker       = False
    membership_type = user.usermembership.membership.membership_type

    try:
        user.tasker
        is_tasker = True
    except:
        is_tasker = False

    dashboard_type               = 'landlord'
    if is_tasker:
        dashboard_type           = 'tasker'

    form = CurrentDashForm()
    form.fields['dashboard_types'].initial = dashboard_type

    if request.method == 'POST':
            form = CurrentDashForm(request.POST)
            if form.is_valid():
                dashboard_type = form.cleaned_data.get("dashboard_types")



    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form
    }
    return render(request, 'dashboards/dashboard-content-main.html', context)
