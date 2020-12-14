from django.contrib import messages
from django.shortcuts import render, redirect

from buyandsell.models import Offer, Posting
from memberships.views import get_user_membership
from rentanything.models import Listing, Booking
from .forms import CurrentDashForm
from .models import TenantVerification
from accounts.models import ChatRoom, ChatRoomMessage, Notification
from django.urls import resolve
from django.contrib.auth.decorators import login_required
from rentals.models import SfvDay, SfvApplication, House
from django.http import HttpResponse



# Create your views here.
@login_required
def dashboard_landlord(request):
    user            = request.user
    print(user)
    is_tasker       = False
    membership_type = get_user_membership(request).membership
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = 'dash'
    dash_active2    = None

    try:
        user.tasker
        is_tasker = True
    except:
        is_tasker = False

    dashboard_type               = 'landlord'

    form = CurrentDashForm()
    print('2')
    form.fields['dashboard_types'].initial = dashboard_type


    if current_url == 'dashboard':
            template = 'dashboards/dash/screen_content/landlord/listings.html'
            dash_active2 = 'landlord_listings'

    elif current_url == 'landlord_applications':
            template = 'dashboards/dash/screen_content/landlord/applications.html'
            dash_active2 = 'landlord_applications_all'

    elif current_url == 'landlord_schedule_for_viewing':
            template = 'dashboards/dash/screen_content/landlord/schedule_for_viewing.html'
            dash_active2 = 'landlord_listing_sfv'

    elif current_url == 'landlord_applications_comparison':
            template = 'dashboards/dash/screen_content/landlord/comparison.html'
            dash_active2 = 'landlord_applications_comparison'

    elif current_url == 'landlord_tenants':
            template = 'dashboards/dash/screen_content/landlord/tenants.html'
            dash_active2 = 'landlord_tenants'

    elif current_url == 'landlord_tenants_verification':
            template = 'dashboards/dash/screen_content/landlord/verification.html'
            dash_active2 = 'landlord_tenants_verification'

    elif current_url == 'landlord_rental_insurance':
            template = 'dashboards/dash/screen_content/landlord/rental_insurance.html'
            dash_active2 = 'landlord_rental_insurance'

    elif current_url == 'landlord_services':
            template = 'dashboards/dash/screen_content/landlord/services.html'
            dash_active2 = 'landlord_services'
    else:
            template = 'dashboards/dash/screen_content/landlord/listings.html'
            dash_active2 = 'landlord_listing_all'

    print('4')
    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
    }
    print('5' , template, dash_active2)
    return render(request, template, context)


@login_required
def dashboard_tenant(request):
    user            = request.user
    membership_type = get_user_membership(request).membership
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = 'dash'
    dash_active2    = None
    dashboard_type  = 'tenant'


    if current_url == 'dashboard_tenant':
            template = 'dashboards/dash/screen_content/tenant/tenant_on.html'
            dash_active2 = 'tenant_on'

    elif current_url == 'tenant_applications':
            template = 'dashboards/dash/screen_content/tenant/applications.html'
            dash_active2 = 'tenant_applications_all'

    elif current_url == 'tenant_schedule_for_viewing':
            template = 'dashboards/dash/screen_content/tenant/schedule_for_viewing.html'
            dash_active2 = 'tenant_applications_sfv'

    elif current_url == 'tenant_rental_insurance':
            template = 'dashboards/dash/screen_content/tenant/rental_insurance.html'
            dash_active2 = 'tenant_ri_all'

    elif current_url == 'tenant_services':
            template = 'dashboards/dash/screen_content/tenant/services.html'
            dash_active2 = 'tenant_services_all'
    else:
            template = 'dashboards/dash/screen_content/landlord/listings.html'
            dash_active2 = 'tenant_applications_all'

    print('4')
    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
    }
    print('5' , template)
    return render(request, template, context)



@login_required
def dashboard_tasker(request):
    print("1")
    user            = request.user
    is_tasker       = False
    membership_type = get_user_membership(request).membership
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = 'dash'
    dash_active2    = None
    dashboard_type   = 'tasker'

    form = CurrentDashForm()
    print('2')
    form.fields['dashboard_types'].initial = dashboard_type


    if current_url == 'dashboard_tasker':
            dash_active2 = 'tasker_tasks_all'
            template = 'dashboards/dash/screen_content/tasker/tasks.html'

    elif current_url == 'tasker_manage_schedule':
            dash_active2 = 'tasker_tasks_ms'
            template = 'dashboards/dash/screen_content/tasker/manage_schedule.html'

    elif current_url == 'tasker_web_dev':

            dash_active2 = 'tasker_wd_all'
            template = 'dashboards/dash/screen_content/tasker/web_dev.html'

    else:
            dash_active2 - 'tasker_tasks_all'
            template = 'dashboards/dash/screen_content/tasker/tasks.html'

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

@login_required
def dashboard_rentanything(request):
    user            = request.user
    membership_type = get_user_membership(request).membership
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = 'dash'
    dash_active2    = None
    dashboard_type   = 'rentanything'

    form = CurrentDashForm()
    form.fields['dashboard_types'].initial = dashboard_type


    if current_url == 'dashboard_rentanything':
            dash_active2 = 'rentanything_listings'
            template = 'dashboards/dash/screen_content/rentanything/listings.html'

    elif current_url == 'rentanything_applications':
            dash_active2 = 'rentanything_applications_all'
            template = 'dashboards/dash/screen_content/rentanything/applications.html'

    elif current_url == 'rentanything_applications_accepted':
            dash_active2 = 'rentanything_applications_accepted'
            template = 'dashboards/dash/screen_content/rentanything/applications_accepted.html'

    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
        "listings"            : Listing.objects.filter(user=user),
        "bookings"            : Booking.objects.all(),
    }
    return render(request, template, context)

@login_required
def dashboard_buyandsell(request):
    user            = request.user
    membership_type = get_user_membership(request).membership
    current_url     = resolve(request.path_info).url_name
    template        = None
    context         = None
    dash_active1    = 'dash'
    dash_active2    = None
    dashboard_type   = 'buyandsell'

    form = CurrentDashForm()
    form.fields['dashboard_types'].initial = dashboard_type


    if current_url == 'dashboard_buyandsell':
            dash_active2 = 'buyandsell_postings'
            template = 'dashboards/dash/screen_content/buyandsell/postings.html'

    elif current_url == 'buyandsell_applications':
            dash_active2 = 'buyandsell_applications_all'
            template = 'dashboards/dash/screen_content/buyandsell/applications.html'

    elif current_url == 'buyandsell_applications_accepted':
            dash_active2 = 'buyandsell_applications_accepted'
            template = 'dashboards/dash/screen_content/buyandsell/applications_accepted.html'

    context = {
        "dashboard_type"      : dashboard_type,
        "membership_type"     : membership_type,
        'form'                : form,
        "dash_active1"        : dash_active1,
        "dash_active2"        : dash_active2,
        "postings"            : Posting.objects.filter(user=user),
        "offers"            : Offer.objects.all(),
    }
    return render(request, template, context)

@login_required
def chats(request, pk=None):
    dash_active1 = 'chats'
    template = 'dashboards/chats/chats-detail.html'
    current_url = resolve(request.path_info).url_name
    context = {}

    if current_url == 'chats':
        context['empty'] = True

    elif current_url == 'chats_detail':
        context['chatroom'] = ChatRoom.objects.filter(pk=pk).first()
        if request.user in context['chatroom'].users.all() or request.user.is_superuser:
            if request.method == "POST":
                if request.POST.get('message'):
                    ChatRoomMessage.objects.create(sender=request.user, text=request.POST.get('message'),
                                                   chatroom_id=pk)
                elif request.POST.get('hidden'):
                    context['chatroom'].users.remove(request.user)
                    if context['chatroom'].users.all().count() == 0:
                        ChatRoomMessage.objects.filter(chatroom=context['chatroom']).delete()
                        context['chatroom'].delete()
                    messages.success(request, "You have left the chatroom.")
                    return redirect('chats')
                return redirect('chats_detail', pk=pk)
            else:
                chatroom_messages = []
                for chatroom_message in ChatRoomMessage.objects.filter(chatroom=context['chatroom']):
                    chatroom_messages.append(chatroom_message)
                    if chatroom_message.sender != request.user:
                        chatroom_message.read = True
                        chatroom_message.save()
                context['chatroom_messages'] = chatroom_messages

    chatrooms = {}
    for chatroom in request.user.profile.get_chatrooms:
        chatrooms[chatroom] = chatroom.is_unread(user=request.user)

    context['dash_active1'] = dash_active1
    context['chatrooms'] = chatrooms

    return render(request, template, context)

@login_required
def notifications(request, pk=None):
    dash_active1 = 'notifications'
    template = 'dashboards/notifications/notifications-detail.html'
    current_url = resolve(request.path_info).url_name
    context = {}

    if current_url == 'notifications':
        context['empty'] = True

    elif current_url == 'notifications_detail':
        context['notification'] = Notification.objects.filter(pk=pk).first()
        if request.user == context['notification'].user:
            context['notification'].read = True
            context['notification'].save()

    notifications = []
    for notification in Notification.objects.filter(user=request.user):
        notifications.append(notification)

    context['dash_active1'] = dash_active1
    context['notifications'] = notifications

    return render(request, template, context)

@login_required
def email(request):
    dash_active1 = 'email'
    template = 'dashboards/email/email.html'
    context = {
       'dash_active1' : 'email'
    }
    return render(request, template, context)

@login_required
def social(request):
    dash_active1 = 'social'
    template = 'dashboards/social/social.html'
    context = {
       'dash_active1' : 'social'
    }
    return render(request, template, context)


@login_required
def sfv_day_select(request):
    sfv_id = request.GET.get('sfv_id')
    sfv_day = SfvDay.objects.filter(id=sfv_id)
    if not sfv_day:
        return HttpResponse("error")
    else:
        sfv_day = sfv_day[0]
        if sfv_day.selected or sfv_day.accepted:
            return HttpResponse("error")


    print(sfv_day)
    sfv_application = sfv_day.sfv_application

    #Deselect everything.
    for x in sfv_application.sfvday_set.all():
         SfvDay.objects.filter(id=x.id).update(selected=False)

    #Select the day
    sfv_day_updated = SfvDay.objects.filter(id=sfv_id).update(selected=True)
    if sfv_day_updated:
        return HttpResponse("done")

    return HttpResponse("Done")

@login_required
def sfv_day_accept(request):
    sfv_id = request.GET.get('sfv_id')
    sfv_day = SfvDay.objects.filter(id=sfv_id)

    sfv_application = sfv_day[0].sfv_application

    if not sfv_day:
        return HttpResponse("error")
    else:
        sfv_day = sfv_day[0]
        if not sfv_day.selected or sfv_day.accepted:
              return HttpResponse("error")

    #Do
    sfv_day = SfvDay.objects.filter(id=sfv_id).update(accepted=True)
    if not sfv_day:
        return HttpResponse("error")

    SfvApplication.objects.filter(id=sfv_application.id).update(scheduled=True)


    return HttpResponse("done")

@login_required
def delete_listing(request):
    ad_id = request.GET.get('ad_id')
    try:
            listing = House.objects.filter(id=ad_id).delete()

            if listing:
                return HttpResponse("good")
            else:
                return HttpResponse("error")
    except:
        return HttpResponse("error")


@login_required
def tenant_verification(request):
    tv_name = request.GET.get('tv_name')
    tv_phone = request.GET.get('tv_phone')
    tv_address = request.GET.get('tv_address')
    tv_notes = request.GET.get('tv_notes')
    print(tv_name, tv_phone, tv_address, tv_notes)

    TenantVerification.objects.create(landlord=request.user.landlord, name=tv_name, phone_number=tv_phone, notes=tv_notes, address=tv_address)

    return HttpResponse("hi")
