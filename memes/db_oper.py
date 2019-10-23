import logging
from memes.models import MemesUsersLikes
log = logging.getLogger("core.corelogger")


class Selections:

    @staticmethod
    def get_likes(meme_obj):
        return MemesUsersLikes.objects.filter(meme=meme_obj, like=1)

    @staticmethod
    def get_dislikes(meme_obj):
        return MemesUsersLikes.objects.filter(meme=meme_obj, like=-1)
