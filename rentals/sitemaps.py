from django.contrib.sitemaps import Sitemap
from rentals.models import House


class HouseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return House.objects.all()