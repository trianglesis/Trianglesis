
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from core.models import AuthUser
from memes.models import MemesObject, MemesUsersComments, MemesUsersLikes, MemesTubes

import logging
log = logging.getLogger("core.corelogger")

User = get_user_model()


class MemeActions:

    @staticmethod
    def delete_meme(meme_obj, user):
        post_author = AuthUser.objects.get(id=user.id)
        MemesObject.objects.get(
            id=meme_obj.id,
            author=post_author
        ).delete()

    @staticmethod
    def post_meme(meme_obj, user):
        # TODO: Make a method to post meme
        pass


class Likes:
    @staticmethod
    def like_meme(meme_obj, user, like=1):
        user_author = AuthUser.objects.get(id=user.id)
        log.debug("Liking meme!")
        like, is_created = MemesUsersLikes.objects.get_or_create(
            author=user_author, meme=meme_obj, like=like
        )
        return like

    @staticmethod
    def remove_like_meme(meme_obj, user):
        user_author = AuthUser.objects.get(id=user.id)
        log.debug("Removing a like!")
        MemesUsersLikes.objects.filter(
            author=user_author, meme=meme_obj, like=1,
        ).delete()

    @staticmethod
    def is_liked(meme_obj, user, like=1):
        if not user.is_authenticated:
            return False
        user_author = AuthUser.objects.get(id=user.id)
        likes = MemesUsersLikes.objects.filter(
            author=user_author, meme=meme_obj, like__gt=0
        )
        return likes.exists()

    def liking(self, meme_obj, user):
        is_liked = self.is_liked(meme_obj, user, like=1)
        log.debug("Currently is_liked: %s", is_liked)
        if not is_liked:
            self.like_meme(meme_obj, user, like=1)
            return 'liked'
        else:
            self.remove_like_meme(meme_obj, user)
            return 'unliked'

    @staticmethod
    def all_likes(meme_obj, like=1):
        return MemesUsersLikes.objects.filter(meme=meme_obj, like__gt=0)


class Dislikes:

    @staticmethod
    def dislike_meme(meme_obj, user, like=-1):
        user_author = AuthUser.objects.get(id=user.id)
        log.debug("DisLiking meme!")
        dislike, is_created = MemesUsersLikes.objects.get_or_create(
            author=user_author, meme=meme_obj, like=-1
        )
        return dislike

    @staticmethod
    def remove_dislike_meme(meme_obj, user):
        user_author = AuthUser.objects.get(id=user.id)
        log.debug("Removing a dislike!")
        MemesUsersLikes.objects.filter(
            author=user_author, meme=meme_obj, like=-1
        ).delete()

    @staticmethod
    def is_disliked(meme_obj, user, like=-1):
        if not user.is_authenticated:
            return False
        user_author = AuthUser.objects.get(id=user.id)
        dislike = MemesUsersLikes.objects.filter(
            author=user_author, meme=meme_obj, like__lt=0
        )
        return dislike.exists()

    def disliking(self, meme_obj, user):
        is_disliked = self.is_disliked(meme_obj, user, like=-1)
        log.debug("Currently is_disliked: %s", is_disliked)
        if not is_disliked:
            self.dislike_meme(meme_obj, user, like=-1)
            return 'disliked'
        else:
            self.remove_dislike_meme(meme_obj, user)
            return 'undisliked'

    @staticmethod
    def all_dislikes(meme_obj, like=-1):
        return MemesUsersLikes.objects.filter(meme=meme_obj, like__lt=0)


class Comments:

    @staticmethod
    def leave_comment(meme_obj, user, comment):
        user_author = AuthUser.objects.get(id=user.id)
        comment, is_added = MemesUsersComments.objects.get_or_create(
            author=user_author, meme=meme_obj, comment=comment,
        )
        return comment

    @staticmethod
    def delete_comment(comment_obj, user):
        user_author = AuthUser.objects.get(id=user.id)
        MemesUsersComments.objects.filter(
            author=user_author, comment_obj=comment_obj
        ).delete()

    @staticmethod
    def get_all_comments(meme_obj):
        comments = MemesUsersComments.objects.filter(meme=meme_obj)
        log.debug("get_all_comments -> comments: %s", len(comments))
        return comments


class TubeActions:

    @staticmethod
    def join_public_tube(tube_obj, user):
        user_author = AuthUser.objects.get(id=user.id)
        tube_obj.tube_members.add(user_author)
        return tube_obj.tube_members.all()

    @staticmethod
    def leave_tube(tube_obj, user):
        user_author = AuthUser.objects.get(id=user.id)
        is_admin = tube_obj.tube_admin
        if not user_author == is_admin:
            log.debug("<=TubeActions=> leave_tube -> not is_admin: %s != %s ", is_admin, user_author)
            tube_obj.tube_members.remove(user_author)
        else:
            log.warning("<=TubeActions=> leave_tube -> Tube admin cannot leave the tube! %s == %s", user_author, is_admin)
        return tube_obj.tube_members.all()
