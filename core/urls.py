"""

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
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^$', views.mainpage_widgets, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^main_panel/', views.main_panel, name='main_panel'),

    # Django registration:
    url(r'^accounts/', include('django_registration.backends.activation.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # Includes:
    url(r'^memes/', include('memes.urls')),
    url(r'^api/v1/', include('memes.api.urls')),
    url(r'^ajax/', include('memes.api.urls')),
    # url(r'^api-auth/', include('rest_framework.urls')),
    url('rest-auth/', include('rest_auth.urls')),

    url(r'^banking/', include('banking.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
