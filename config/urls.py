"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from rentals.sitemaps import HouseSitemap
from services.sitemaps import ServiceSitemap
from django.views.generic import TemplateView


sitemaps = {
    'houses': HouseSitemap,
    'services': ServiceSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('finance/',include('finances.urls')),
    path('rentals/',include('rentals.urls')),
    path('services/',include('services.urls')),
    path('rentanything/', include('rentanything.urls')),
    path('buyandsell/', include('buyandsell.urls')),
    path('deliveranything/', include('deliveranything.urls')),
    path('businesses/', include('businesses.urls')),
    path('faq/',include('faq.urls')),
    path('',include('agreements.urls')),
    path('membership/',include('memberships.urls')),
    path('dashboard/',include('dashboards.urls')),
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
