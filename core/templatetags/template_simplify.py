"""
Template tags for saving time and space in templates
"""
import logging
from django import template
from django.template import loader
from django.template import loader, Template, Context


register = template.Library()
# reg_filter = template.Library.filter()
log = logging.getLogger("core.corelogger")


@register.filter(name='escape_extra')
def escape_extra(value):
    replacing = [".", ",", "!", ":", ";", "#"]
    for to_replace in replacing:
        if to_replace in value:
            return value.replace(to_replace, "_")
        else:
            return value


@register.filter(name='replace_dot')
def replace_dot(value):
    return value.replace(".", "_")


@register.filter(name='replace_exclamation')
def replace_exclamation(value):
    return value.replace("!", "_")


@register.simple_tag(takes_context=True)
def subject_on_page(context, subject):
    html_t = loader.get_template('root/small_elements/page_subject.html')
    contxt = dict(SUBJECT=subject)
    return html_t.render(contxt)


# @register.simple_tag(takes_context=True)
# def check_url(context):
#     log.debug("Current url path is: %s", request.path)
#     return True


@register.simple_tag()
def octicon(icon_name, size, side=None, margin=None):
    if side and margin:
        html = Template('{% load static %}<img style="height:{{size}}px;width:{{size}}px;margin-{{side}}: {{margin}}em;" src="/static/octicons/svg/{{icon_name}}.svg" alt="{{icon_name}}" />')
        c = Context(dict(size=size, side=side, margin=margin, icon_name=icon_name))
    else:
        html = Template('{% load static %}<img style="height:{{size}}px;width:{{size}}px;" src="/static/octicons/svg/{{icon_name}}.svg" alt="{{icon_name}}" />')
        c = Context(dict(size=size, icon_name=icon_name))
    return html.render(c)


@register.simple_tag()
def open_iconic(icon_name, size, side=None, margin=None):
    if side and margin:
        html = Template('{% load static %}<img style="height:{{size}}px;width:{{size}}px;margin-{{side}}: {{margin}}em;" src="/static/open-iconic-master/svg/{{icon_name}}.svg" alt="{{icon_name}}" />')
        c = Context(dict(size=size, side=side, margin=margin, icon_name=icon_name))
    else:
        html = Template('{% load static %}<img style="height:{{size}}px;width:{{size}}px;" src="/static/open-iconic-master/svg/{{icon_name}}.svg" alt="{{icon_name}}" />')
        c = Context(dict(size=size, icon_name=icon_name))
    return html.render(c)