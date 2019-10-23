from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static

from banking.views import *

urlpatterns = [

    url(r'^main/', BankingMain.main, name='main'),

]