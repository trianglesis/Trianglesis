"""
Template tags for saving time and space in templates
"""
import logging
import re

from django import template
from django.template import loader
from django.conf import settings

from memes.db_oper import Selections
from core.models import AuthUser

register = template.Library()
# reg_filter = template.Library.filter()
log = logging.getLogger("core.corelogger")

allowed_url_ext = dict(
    mp_4=re.compile(r'.*\.mp4'),
    webm=re.compile(r'.*\.webm'),
    webp=re.compile(r'.*\.webp'),
    gif=re.compile(r'.*\.gif'),
    jpg=re.compile(r'.*\.jpg'),
    png=re.compile(r'.*\.png'),
)
known_url = dict(
    # https://play.google.com/music/m/Tsk3z7lsp2u4kdzgwy4i44olv5i?t=Ready_To_Blast_Original_Mix_-_Cyberpunkers_Far_Too_Loud
    gif=re.compile(r'(?P<protocol>http|https)://(?P<source>\S+)/(?P<file>\S+)(?P<extension>\.gif)'),
    mp_4=re.compile(r'(?P<protocol>http|https)://(?P<source>\S+)/(?P<file>\S+)(?P<extension>\.mp4)'),
    webm=re.compile(r'(?P<protocol>http|https)://(?P<source>\S+)/(?P<file>\S+)(?P<extension>\.webm)'),

    coub=re.compile(r'(?P<protocol>http|https)://coub\.com/view/(?P<code>\S+)'),
    youtu_be=re.compile(r'(?P<protocol>http|https)://youtu.be/(?P<code>\w+)(?=\?|)(?P<timecode>\?t=\d+|)'),
    youtube=re.compile(r'(?P<protocol>http|https)://www\.youtube\.com/watch\?v=(?P<code>\w+)'),
    google_mus=re.compile(r'(?P<protocol>http|https)://play\.google\.com/music/m/(?P<code>\S+)(?=\?|)(\?t=(?P<title>\S+))'),
)

frames_types = dict(
    gif=loader.get_template('root/memes/frames/webm_iframe.html'),
    mp_4=loader.get_template('root/memes/frames/webm_iframe.html'),
    webm=loader.get_template('root/memes/frames/webm_iframe.html'),
    coub=loader.get_template('root/memes/frames/coub_iframe.html'),
    youtu_be=loader.get_template('root/memes/frames/youtube_iframe.html'),
    youtube=loader.get_template('root/memes/frames/youtube_iframe.html'),
    google_mus=loader.get_template('root/memes/frames/g_music_iframe.html'),
    else_t=loader.get_template('root/memes/frames/hyperlink.html'),
)


@register.simple_tag()
def video_frame(url):
    log.debug("video_frame url: %s", url)
    for k, v in known_url.items():
        if re.match(v, url):
            log.debug("This is file: '%s' - matches: %s ", k, v)
            parsed = re.match(v, url)
            if parsed:
                log.debug("File '%s' args: %s ", k, parsed)
                parsed_d = parsed.groupdict()
                parsed_d.update(TAG_URL=url)
                parsed_d.update(file_type=k)
                log.debug("File type - %s", k)
                log.debug("'%s' parsed_d %s", k, parsed_d)

                extension = parsed_d.get('extension', False)
                if extension:
                    pass
                    log.debug("This file '%s' extension: %s", k, extension)

                iframe_template = frames_types.get(k, None)
                log.debug("Template for '%s' - %s", k, iframe_template)
                return iframe_template.render(parsed_d)
    else:
        return frames_types['else_t'].render(dict(TAG_URL=url))

