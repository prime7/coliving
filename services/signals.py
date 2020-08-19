from django.db.models.signals import pre_save
from django.dispatch import receiver
from services.models import Service



def create_slug(instance,new_slug = None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Service.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug


@receiver(pre_save,sender=Service)
def pre_save_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)