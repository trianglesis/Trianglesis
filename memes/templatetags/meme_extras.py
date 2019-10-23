"""
Template tags for saving time and space in templates
"""
import logging

from django import template
from django.template import loader
from django.conf import settings

from memes.db_oper import Selections

from core.models import AuthUser
from memes.models import MemesTubes, MemesUsersLikes, MemesUsersComments

register = template.Library()
# reg_filter = template.Library.filter()
log = logging.getLogger("core.corelogger")


@register.simple_tag(takes_context=True)
def left_col_draw(context, **kwargs):
    html_t = loader.get_template('root/memes/left_col.html')
    log.debug("KWARGS: %s", kwargs)
    contxt = dict(context=context, KWARGS=kwargs)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def center_col_draw(context, memes):
    html_t = loader.get_template('root/memes/center_col.html')
    contxt = dict(context=context, MEMES=memes, MEDIA_URL=settings.MEDIA_URL)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def right_col_draw(context):
    html_t = loader.get_template('root/memes/right_col.html')
    contxt = dict(context=context)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def meme_block_draw(context, meme_obj, meme_solo=False):
    html_t = loader.get_template('root/memes/widgets/meme_block.html')
    contxt = dict(context=context, MEME=meme_obj, MEME_SOLO=meme_solo)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def paginator_draw(context, objects_to_paginate):
    html_t = loader.get_template('root/memes/widgets/paginator.html')
    contxt = dict(context=context, ITEMS=objects_to_paginate)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def get_comments_count(context, meme_obj):
    comments_count = MemesUsersComments.objects.filter(meme=meme_obj)
    return len(comments_count)


@register.simple_tag(takes_context=True)
def get_comments_obj(context, meme_obj):
    html_t = loader.get_template('root/memes/widgets/meme_comments.html')
    comments_objs = MemesUsersComments.objects.filter(meme=meme_obj)
    contxt = dict(COMMENTS=comments_objs)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def get_likes_count(context, meme_obj):
    likes_count = MemesUsersLikes.objects.filter(meme=meme_obj, like=1)
    return len(likes_count)


@register.simple_tag(takes_context=True)
def get_dislikes_count(context, meme_obj):
    dislikes_count = MemesUsersLikes.objects.filter(meme=meme_obj, like=-1)
    return len(dislikes_count)


@register.simple_tag(takes_context=True)
def get_likes_obj(context, meme_obj, type='like'):
    html_t = loader.get_template('root/memes/widgets/memes_likes.html')
    like_dis_f = dict(
        like=Selections.get_likes,
        dislike=Selections.get_dislikes,
    )
    # likes_objs = Selections.get_likes(meme_obj, type)
    likes_f = like_dis_f.get(type, None)
    if likes_f:
        likes_objs = likes_f(meme_obj)
    else:
        likes_objs = {}

    contxt = dict(LIKES=likes_objs, MEME=meme_obj, action_type=type)
    return html_t.render(contxt)


@register.simple_tag(takes_context=True)
def like_dislike(context, meme_obj, user, like):
    log.debug("meme_obj %s", meme_obj)
    log.debug("user %s", user)
    log.debug("like %s", like)


@register.simple_tag(takes_context=True)
def get_user_admin_tubes(context, user, status):
    html_t = loader.get_template('root/memes/widgets/tubes_user_admin.html')

    log.debug("user: %s", user)
    auth_user = AuthUser.objects.get(username=user)

    if status == 'admin':
        mode = 'Admin'
        my_admin_tubes = MemesTubes.objects.filter(tube_admin=auth_user)
        my_tubes = my_admin_tubes
    elif status == 'member':
        mode = 'Member'
        my_member_tubes = MemesTubes.objects.filter(tube_members=auth_user)
        my_tubes = my_member_tubes
    else:
        mode = 'Member'
        my_member_tubes = MemesTubes.objects.filter(tube_members=auth_user)
        my_tubes = my_member_tubes

    contxt = dict(MY_TUBES=my_tubes, mode=mode)
    return html_t.render(contxt)
