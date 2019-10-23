"""
https://www.django-rest-framework.org/tutorial/quickstart/
"""

from rest_framework import serializers
from core.models import AuthUser
from memes.models import MemesObject, MemesUsersComments, MemesUsersLikes, MemesTubes
from memes import services as likes_services
from django.contrib.auth import get_user_model

import logging
log = logging.getLogger("core.corelogger")

User = get_user_model()


class MemesAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'last_login',
            'date_joined',
            # SERVICE: DO NOT SHOW FOR ALL
            #'email',
            #'is_staff',
            #'is_active',
            #'is_superuser',
        )


class MemesObjectSerializer(serializers.ModelSerializer):
    """
    http://coreymaynard.com/blog/performing-ajax-post-requests-in-django/
    https://realpython.com/django-and-ajax-form-submissions/
    """
    is_liked = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    # likes = serializers.SerializerMethodField()
    # dislikes = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()

    log.debug("MemesObjectSerializer meme!")

    class Meta:
        model = MemesObject
        fields = (
            'id',
            'title',
            'tags',
            'author',
            'username',
            'image',
            'file',
            'link',
            'text',
            'hypertext',
            'tubes',
            'pub_date',
            'is_liked',
            'is_disliked',
            # 'likes',
            # 'dislikes',
            # 'comments',
        )

    def get_is_liked(self, obj):
        log.debug("MemesObjectSerializer -> get_is_liked!")
        user = self.context.get('request').user
        return likes_services.Likes.is_liked(obj, user)

    def get_is_disliked(self, obj):
        log.debug("MemesObjectSerializer -> get_is_disliked!")
        user = self.context.get('request').user
        return likes_services.Dislikes.is_disliked(obj, user)

    @staticmethod
    def get_username(obj):
        return obj.author.username

    # @staticmethod
    # def get_comments(obj):
    #     log.debug("MemesObjectSerializer -> get_comments!")
    #     comments = likes_services.Comments.get_all_comments(obj)
    #     serializer = MemesUsersCommentsSerializer(comments, many=True)
    #     return serializer.data
    #
    # @staticmethod
    # def get_likes(obj):
    #     log.debug("MemesObjectSerializer -> get_likes!")
    #     likes = likes_services.Likes.all_likes(obj)
    #     serializer = MemesUsersLikesSerializer(likes, many=True)
    #     return serializer.data
    #
    # @staticmethod
    # def get_dislikes(obj):
    #     log.debug("MemesObjectSerializer -> get_dislikes!")
    #     dislikes = likes_services.Dislikes.all_dislikes(obj)
    #     serializer = MemesUsersLikesSerializer(dislikes, many=True)
    #     return serializer.data


class MemesUsersCommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = MemesUsersComments
        fields = (
            'id',
            'author',
            'username',
            'meme',
            'comment',
            'pub_date',
        )

    @staticmethod
    def get_username(obj):
        return obj.author.username


class MemesUsersLikesSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = MemesUsersLikes
        fields = (
            'id',
            'author',
            'username',
            'meme',
            'like',
            'pub_date',
        )

    @staticmethod
    def get_username(obj):
        return obj.author.username


class MemesTubesSerializer(serializers.ModelSerializer):
    tube_admin_username = serializers.SerializerMethodField()
    # tube_members_names = serializers.SerializerMethodField()

    class Meta:
        model = MemesTubes
        fields = (
            'id',
            'tube',
            'tube_admin',
            'tube_admin_username',
            'tube_members',
            # 'tube_members_names',
            'is_private',
        )

    @staticmethod
    def get_tube_admin_username(obj):
        return obj.tube_admin.username

    @staticmethod
    def get_tube_members_names(obj):
        serializer = MemesAuthorSerializer(obj.tube_members, many=True)
        return serializer.data
