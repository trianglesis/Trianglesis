from django.contrib import admin
from memes.models import MemesObject, MemesUsersComments, MemesUsersLikes, MemesTubes
from banking.models import *

# from django.contrib import admin
from .models import *
import logging

log = logging.getLogger("core.corelogger")

"""
https://docs.djangoproject.com/en/2.2/ref/models/fields/#slugfield
https://docs.djangoproject.com/en/2.2/ref/models/fields/#imagefield
https://docs.djangoproject.com/en/2.2/topics/db/examples/one_to_one/
https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_many/
https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_one/
https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey.on_delete
"""


# @admin.register(MemesAuthor)
# class MemesAuthorAdmin(admin.ModelAdmin):
#     list_display = ('user', 'nickname')
#     # list_editable = ()
#     list_filter = ('user', 'nickname')
#     ordering = ('nickname',)
#     search_fields = ('nickname',)
#     fieldsets = (
#         ('Memes User', {
#             'description': "Memes user",
#             'fields': ('user', 'nickname')}
#          ),
#     )


@admin.register(MemesTubes)
class MemesTubesAdmin(admin.ModelAdmin):
    list_display = (
        'tube',
        'tube_admin',
        'is_private',
    )
    # list_editable = ()
    list_filter = ('tube', 'tube_admin')
    ordering = ('tube',)
    search_fields = ('tube',)
    fieldsets = (
        ('Tubes', {
            'description': "Tubes",
            'fields': ('tube', 'tube_admin',
                       'tube_members',
                       'is_private'
                       )}
         ),
    )


@admin.register(MemesUsersComments)
class MemesUsersCommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'pub_date', 'meme')
    # list_editable = ()
    list_filter = ('author', 'pub_date',)
    ordering = ('pub_date',)
    readonly_fields = ('pub_date',)
    search_fields = ('author', 'comment', 'pub_date',)
    fieldsets = (
        ('Comment', {
            'description': "User Comment:",
            'fields': ('author', 'comment', 'pub_date', 'meme')}
         ),
    )


@admin.register(MemesUsersLikes)
class MemesUsersLikesAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'meme', 'like')
    # list_editable = ()
    list_filter = ('author', 'pub_date',)
    ordering = ('pub_date',)
    readonly_fields = ('pub_date',)
    search_fields = ('author', 'pub_date',)
    fieldsets = (
        ('Like', {
            'description': "User Like:",
            'fields': ('author', 'pub_date', 'meme', 'like')}
         ),
    )


@admin.register(MemesObject)
class MemesObjectAdmin(admin.ModelAdmin):
    # model = MemesObject
    list_display = [
        'title', 'tags', 'author',
        'image', 'link', 'file', 'text', 'hypertext',
        'pub_date',
        # 'get_likes',
        # 'comments',
        'tubes',
    ]
    # list_editable = ()
    ordering = ('pub_date',)
    list_filter = ('author', 'pub_date', 'tubes',)
    readonly_fields = ('pub_date',)
    search_fields = ('title', 'tags', 'pub_date', 'author',)
    fieldsets = (
        ('Meme Metadata', {
            'description': "Meme:",
            'fields': ('title', 'tags', 'author', 'pub_date', 'tubes')}
         ),
        ('Meme image', {
            'description': "Meme image:",
            'fields': ('image',)},
         ),
        ('Meme link', {
            'description': "Meme link:",
            'fields': ('link',)},
         ),
        ('Meme file', {
            'description': "Meme file:",
            'fields': ('file',)},
         ),
        ('Meme Text', {
            'description': "Meme text:",
            'fields': ('text',)},
         ),
        ('Meme hypertext', {
            'description': "Meme hypertext:",
            'fields': ('hypertext',)},
         ),
        # ('Meme Comments & Likes', {
        #     'description': "Meme Metadata:",
        #     'fields': ('get_likes', 'comments')},
        #  ),
    )

    # def get_likes(self, obj):
    #     return obj.memes_likes
    #
    # get_likes.author = 'memes_likes__author'
    # get_likes.pub_date = 'memes_likes__pub_date'
    #
    # def comments(self, obj):
    #     return obj.memes_comments
    #
    # comments.author = 'memes_comments__author'
    # comments.comment = 'memes_comments__comment'
    # comments.pub_date = 'memes_comments__pub_date'


# admin.site.register(AuthUser)
@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_superuser',
        'is_staff',
        'is_active',
        'last_login',
        'date_joined',
    )
    # list_editable = ()
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    ordering = ('date_joined',)
    search_fields = ('username',)
    readonly_fields = (
        'password',
        'last_login',
        'date_joined',
    )
    fieldsets = (
        ('Memes User', {
            'description': "Memes user",
            'fields': ('is_superuser',
                       'username',
                       # 'first_name',
                       # 'last_name',
                       # 'email',
                       'is_staff',
                       'is_active',)}
         ),
    )


# admin.site.register(AuthUserGroups)
# admin.site.register(AuthUserUserPermissions)
# admin.site.register(DjangoAdminLog)
# admin.site.register(DjangoContentType)

# admin.site.register(DjangoMigrations)
@admin.register(DjangoMigrations)
class DjangoMigrationsAdmin(admin.ModelAdmin):
    list_display = (
        'app',
        'name',
        'applied',
    )

# admin.site.register(DjangoSession)
#
# # DjangoCeleryBeat
# admin.site.register(DjangoCeleryBeatCrontabschedule)
# admin.site.register(DjangoCeleryBeatIntervalschedule)
# admin.site.register(DjangoCeleryBeatPeriodictask)
# admin.site.register(DjangoCeleryBeatPeriodictasks)
# admin.site.register(DjangoCeleryBeatSolarschedule)


@admin.register(CardOperations)
class CardOperationsAdmin(admin.ModelAdmin):
    list_display = [
        'account_number',
        'operation_type',
        'operation_date',
        'operation_bank_date',
        'operation_description',
        'operation_sum',
        'operation_currency',
        'operation_sum_by_account_currency',
        'account_currency',
        'company_code',
        # Rels:
        'related_account_number',
        'operation_group',
        'operation_bank',
        'operation_account_type',
    ]
    # list_editable = ()
    ordering = ('operation_date',)
    list_filter = ('account_number', 'operation_bank_date', 'operation_date',
                   'operation_description', 'operation_type')
    readonly_fields = ('operation_date',)
    search_fields = ('operation_type', 'account_number')

    fieldsets = (

        ('Account data', {
            'description': "Account metadata:",
            'fields': ('account_number', 'account_currency', 'operation_type')}
         ),
        ('Operation metadata', {
            'description': "Types and sorts of operations:",
            'fields': ('operation_date', 'operation_bank_date', 'operation_description', 'company_code')
        },
         ),
        ('Financial data', {
            'description': "Meme link:",
            'fields': ('operation_sum', 'operation_currency', 'operation_sum_by_account_currency')},
         ),

        ('Relations data', {
            'description': "Related accounts and descriptions:",
            'fields': ('related_account_number', 'operation_group', 'operation_bank', 'operation_account_type')},
         ),
    )


@admin.register(OperationGroups)
class OperationGroupsAdmin(admin.ModelAdmin):
    list_display = (
        'operation_group_name',
        'operation_description',
        'operation_max_limit',
        'operation_min_limit',
        'operation_limit',
    )
    # list_editable = ()
    list_filter = ('operation_group_name', 'operation_max_limit')
    ordering = ('operation_group_name',)
    search_fields = ('operation_group_name',)
    fieldsets = (
        ('Operation groups', {
            'description': "Operation groups",
            'fields': (
                'operation_group_name',
                'operation_description',
                'operation_max_limit',
                'operation_min_limit',
                'operation_limit',
            )}
         ),
    )


@admin.register(AccountTypes)
class AccountTypesAdmin(admin.ModelAdmin):
    list_display = (
        'account_number',
        'account_custom_type',
        'account_custom_comment',
        'active',
        'user_alias',
    )
    # list_editable = ()
    list_filter = ('account_number', 'account_custom_type', 'active')
    ordering = ('account_number',)
    search_fields = ('account_number', 'account_custom_type')
    fieldsets = (
        ('Account Types', {
            'description': "Account Types",
            'fields': (
                'account_number',
                'account_custom_type',
                'account_custom_comment',
                'active',
                'user_alias',
            )}
         ),
    )


@admin.register(BankAccounts)
class BankAccountsAdmin(admin.ModelAdmin):
    list_display = (
        'account_number',
        'holder_user',
        'holder_name',
        'bank_name',
    )
    # list_editable = ()
    list_filter = ('account_number', 'holder_user', 'bank_name')
    ordering = ('account_number',)
    search_fields = ('account_number', 'holder_user', 'bank_name')
    fieldsets = (
        ('Accounts', {
            'description': "Accounts",
            'fields': (
                'account_number',
                'holder_user',
                'holder_name',
                'bank_name',
            )}
         ),
    )