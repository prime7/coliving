from .models import Membership, UserMembership, Subscription
def get_user_membership(request):
    if not request.user.is_anonymous:
        user_membership_qs = UserMembership.objects.filter(user=request.user)
        if user_membership_qs.exists():
            membership = user_membership_qs.first()
            return {
                "membership" : membership.membership.membership_type
            }
    return {"membership":"None"}

def is_landlord(request):
    if not request.user.is_anonymous:
        user_membership_qs = UserMembership.objects.filter(user=request.user)
        if user_membership_qs.exists():
            membership = user_membership_qs.first()
            if membership.membership.membership_type == 'Landlord':
                return True
    return False

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None