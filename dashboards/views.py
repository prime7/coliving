from django.shortcuts import render
from .forms import CurrentDashForm
from django.urls import resolve

# Create your views here.
def dashboard(request):
    user            = request.user
    is_tasker       = False
    membership_type = user.usermembership.membership.membership_type
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = None
    dash_active2    = None

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


    if current_url == 'sharing':
           template = 'dashboards/dashboard_main_content/dmc/sharing.html'
           dash_active2 = 'sharing'
    else:
        template = 'dashboards/dashboard_main_content/dashboard-content-main.html'
    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
    }
    return render(request, template, context)
