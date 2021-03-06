"""billetterie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Billevent API')


urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^swagger', schema_view),
    url(r'^tickets/', include('ticketgenerator.urls')),
    url(r'^pay/', include('mercanet.urls')),
    url(r'^', include('frontend.urls')) #il faut que ce soit la dernière ligne !!!
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
