"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views
from django.views.generic.base import RedirectView
# from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
]
# captcha url
urlpatterns += [
    path('captcha/', include('captcha.urls'))
]

# Use include() to add paths from the catalog application

urlpatterns += [
    path('catalog/', include('catalog.urls')),
]
# Add URL maps to redirect the base URL to our application
urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]

urlpatterns += [
    path('fav.ico', RedirectView.as_view(url='/static/fav.ico')), ]

urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}, name='media'),
]
# Use static() to add url mapping to serve static files during development (only)
# --------------------------------------
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Use include() to add URLS from the catalog application and authentication system
# from django.urls import include

# Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# Make 404.html and 500.html setting when DEBUG = False


urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]

handler404 = views.page_not_found

handler500 = views.page_error

handler403 = views.page_permission_denied
#  ——————————test popup
urlpatterns += [
    path('testpopud/', include('testInput.urls')),
]
