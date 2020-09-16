from django import template
from ..models import Faq


register = template.Library()

@register.inclusion_tag('faq/templatetags/faqs.html')
def show_faqs(category=None):
    if category:
        faqs = Faq.objects.filter(faq_category=category)
    else:
        faqs = Faq.objects.all()
    return {'faqs': faqs }