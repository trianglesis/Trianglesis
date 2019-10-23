from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.template import loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from core.user_operations import UserCheck
from core.models import AuthUser


# Python logger
import logging

log = logging.getLogger("core.corelogger")


class BankingMain:

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def main(request):
        page_widgets = loader.get_template('root/tubes_space/tube_manage.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> manage(): %s", user_string)