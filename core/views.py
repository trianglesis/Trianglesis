from django.template import loader
from django.http import HttpResponse
from core.user_operations import UserCheck
# Python logger
import logging

log = logging.getLogger("core.corelogger")


def mainpage_widgets(request):
    page_widgets = loader.get_template('root/main/widgets/main_widgets.html')
    user_name, user_string = UserCheck().user_string_f(request)
    log.debug("<=MAIN Widgets=> mainpage_widgets(): %s", user_string)
    widgets = dict(SUBJECT="")
    return HttpResponse(page_widgets.render(widgets, request))


def main_panel(request):
    page_widgets = loader.get_template('root/main/widgets/main_panel.html')
    user_name, user_string = UserCheck().user_string_f(request)
    log.debug("<=MAIN Widgets=> devs_page_widgets(): %s", user_string)
    widgets = dict(SUBJECT="")
    return HttpResponse(page_widgets.render(widgets, request))
