# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import urllib
from urllib import request

from django.db import models
from core.models import AuthUser
from django.template.defaultfilters import slugify


from django.core.files.storage import FileSystemStorage

import logging
log = logging.getLogger("core.corelogger")


def user_image_dir(instance, filename):
    # https://stackoverflow.com/a/34239992/4915733
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    dir_path = u'user_media/pictures/user_{0}/{1}'.format(instance.author.id, request.quote(filename).encode('utf-8'))
    return dir_path


def user_file_dir(instance, filename):
    # https://stackoverflow.com/a/34239992/4915733
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    dir_path = u'user_media/files/user_{0}/{1}'.format(instance.author.id, request.quote(filename).encode('utf-8'))
    return dir_path


class MemesTubes(models.Model):
    tube = models.CharField(max_length=255, unique=True)
    tube_admin = models.ForeignKey(AuthUser, null=True, related_name='tuber', on_delete=models.CASCADE)
    tube_members = models.ManyToManyField(AuthUser, related_name='tubers')
    is_private = models.BooleanField(null=True)
    # TODO: Add short info/description/picture?

    class Meta:
        managed = True
        db_table = 'memes_tubes'

    def __str__(self):
        return '{1} - {0}'.format(self.tube, 'Private' if self.is_private else 'Public')


class MemesObject(models.Model):
    # Meme metadata
    title = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    # One author
    author = models.ForeignKey(AuthUser, on_delete=models.CASCADE, blank=True)

    # Meme data
    image = models.ImageField(
        # storage=images,
        upload_to=user_image_dir,
        null=True, blank=True,
        verbose_name='Image',)
    file = models.FileField(
        # storage=files,
        upload_to=user_file_dir,
        null=True, blank=True,
        verbose_name='File',)

    link = models.URLField(max_length=255, null=True, blank=True)

    text = models.TextField(null=True, blank=True)
    hypertext = models.TextField(null=True, blank=True)

    # Meme metadata
    # One tube
    tubes = models.ForeignKey(MemesTubes, on_delete=models.CASCADE, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    # Many comments
    # comments = models.ForeignKey(MemesUsersComments, on_delete=models.DO_NOTHING, blank=True)
    # Many likes
    # likes = models.ForeignKey(MemesUsersLikes, on_delete=models.DO_NOTHING, blank=True)

    class Meta:
        managed = True
        db_table = 'memes_object'

    def __str__(self):
        return self.title

    # @property
    # def total_likes(self):
    #     return self.likes.count()


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Images(models.Model):
    post = models.ForeignKey(MemesObject, default=None, on_delete=models.DO_NOTHING)
    images = models.ImageField(upload_to=get_image_filename, verbose_name='Image')


class Files(models.Model):
    post = models.ForeignKey(MemesObject, default=None, on_delete=models.DO_NOTHING)
    files = models.ImageField(upload_to=get_image_filename, verbose_name='File')


class MemesUsersComments(models.Model):
    author = models.ForeignKey(AuthUser, related_name="comment_author", on_delete=models.CASCADE, blank=True)
    meme = models.ForeignKey(MemesObject, on_delete=models.CASCADE, blank=True)
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'memes_comments'


class MemesUsersLikes(models.Model):
    author = models.ForeignKey(AuthUser, related_name="like_author", on_delete=models.CASCADE, blank=True)
    meme = models.ForeignKey(MemesObject, related_name="liked_meme", on_delete=models.CASCADE, blank=True)
    like = models.SmallIntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'memes_likes'

    def __str__(self):
        return '{}:{}:{}'.format(self.author.username, self.meme.title, self.like)
