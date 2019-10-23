from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static

from memes.views import Memes, UserSpace, TubeViews

urlpatterns = [

    url(r'^public/', Memes.public,
        name='public'),
    url(r'^my_tubes/', Memes.my_tubes,
        name='my_tubes'),
    url(r'^single_tube/', Memes.single_tube,
        name='single_tube'),

    url(r'^meme/', Memes.meme,
        name='meme'),

    url(r'^meme_posted/(?P<meme_id>\d+)/$', Memes.meme,
        name='meme_posted'),

    url(r'^post_meme/', Memes.post_meme,
        name='post_meme'),

    url(r'^post_multiple/', Memes.post_multiple,
        name='post_multiple'),

    url(r'^delete_single_meme/', Memes.delete_single_meme,
        name='delete_single_meme'),

    # User space
    url(r'^space/', UserSpace.space,
        name='space'),

    # Tubes space
    url(r'^tubes/', TubeViews.list_tubes,
        name='tubes'),
    url(r'^manage_tube/', TubeViews.manage,
        name='manage_tube'),
    
    url(r'^leave_tube/', TubeViews.leave,
        name='leave_tube'),
    url(r'^join_tube/', TubeViews.join,
        name='join_tube'),
    url(r'^delete_tube/', TubeViews.delete,
        name='delete_tube'),

    url(r'^tube_create/', TubeViews.create,
        name='tube_create'),


]