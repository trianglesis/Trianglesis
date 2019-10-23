"""
Testing tags
"""

import logging
import datetime
from django import template
from django.template import loader

register = template.Library()
log = logging.getLogger("core.corelogger")


@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)
