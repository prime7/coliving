from django.shortcuts import render
from .forms import CurrentDashForm
from django.urls import resolve
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    print("1")
    user            = request.user
    is_tasker       = False
    #membership_type = user.usermembership.membership.membership_type
    membership_type = 'premium'
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
    print('2')
    form.fields['dashboard_types'].initial = dashboard_type

    if request.method == 'POST':
            form = CurrentDashForm(request.POST)
            if form.is_valid():
                dashboard_type = form.cleaned_data.get("dashboard_types")

    if current_url == 'applications':
        template = 'dashboards/dash/screen_content/landlord/applications.html'
    else:
        template = 'dashboards/dash/screen_content/landlord/listings.html'

    print('4')
    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
    }
    print('5' , template)
    return render(request, template, context)
