
from django.db.models import Q
from django import forms
from django.forms import ModelChoiceField
from memes.models import MemesObject, MemesTubes, Images, Files, MemesUsersLikes

import logging

log = logging.getLogger("core.corelogger")


class PostFormMeme(forms.ModelForm):
    """
    Validate file:
        - https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
    Custom widgets:
        - https://blog.ihfazh.com/django-custom-widget-with-3-examples.html
    """
    def __init__(self, author_obj, *args, **kwargs):
        super(PostFormMeme, self).__init__(*args, **kwargs)
        self.admin_member_tubes = MemesTubes.objects.filter(Q(tube_admin=author_obj) | Q(tube_members=author_obj))
        tubes_q = self.admin_member_tubes.distinct()
        # values_list = [(tube_q.tube, tube_q.is_private) for tube_q in tubes_q]
        # print(values_list)
        # self.fields['tubes'].tuple = values_list
        self.fields['tubes'].queryset = tubes_q.order_by('is_private')

    class Meta:
        model = MemesObject
        title = forms.CharField(
            help_text='100 characters max.',
            error_messages={'required': 'Please enter a tittle!'},
        )
        tags = forms.CharField(
            help_text='3 or 4 main tags, please.',
            error_messages={'required': 'Please enter some tags!'},
        )
        # tubes = ModelChoiceField(queryset=MemesTubes.objects.all(), to_field_name="tube", empty_label="(Nothing)")
        # upload_to='documents/'
        image = forms.ImageField(
            help_text='jpg, png, webp, gif'
        )
        # upload_to='documents/'
        file = forms.FileField(
            help_text='Small file'
        )
        link = forms.URLField(
            help_text='Post a link to youtube for example, of G-music'
        )
        text = forms.CharField(
            help_text='Short text without formatting, like a tweet'
        )
        hypertext = forms.CharField(
            help_text='Long text with formatting, like a blog post'
        )

        fields = ('title', 'tags', 'image', 'link', 'file', 'text', 'hypertext', 'tubes',)

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 'type': 'text', 'aria-label': 'Post_title',
                'aria-describedby': 'inputGroup-sizing-default'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 'type': 'text', 'aria-label': 'Post_tags',
                'aria-describedby': 'inputGroup-sizing-default'}),

            'tubes': forms.Select(attrs={'class': 'form-control'}),

            'image': forms.ClearableFileInput(attrs={
                'type': 'file',
                'class': 'form-control-file btn btn-sm btn-outline-secondary',
                'id': 'inputGroupImage',
                # 'multiple': True,
            }),
            'file': forms.ClearableFileInput(attrs={
                'type': 'file',
                'class': 'form-control-file btn btn-sm btn-outline-secondary',
                'id': 'inputGroupFile',
                # 'multiple': True,
            }),

            'link': forms.URLInput(attrs={
                'class': 'form-control', 'type': 'text', 'aria-label': 'Small',
                'aria-describedby': 'inputGroup-sizing-sm'}),

            'text': forms.Textarea(attrs={
                'test': 'its working!',
                'class': 'form-control',
                'rows': '4', 'cols': '4',
                'aria-label': 'Short post'
            }),
            'hypertext': forms.Textarea(attrs={
                'test': 'its working!',
                'class': 'form-control',
                'rows': '10', 'cols': '4',
                'aria-label': 'Long post'
            }),
        }


class TubeCreateForm(forms.ModelForm):

    class Meta:
        model = MemesTubes

        tube = forms.CharField()
        is_private = forms.BooleanField()

        fields = ('tube', 'is_private',)

        widgets = {
            'tube': forms.TextInput(attrs={
                'class': 'form-control', 'type': 'text', 'aria-label': 'Post_title',
                'aria-describedby': 'inputGroup-sizing-default'}),
            'is_private': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input position-static isPrivate',
                    'type': 'checkbox',
                    'id': 'gridCheck1',

                }
            )
        }


class ImagesForm(forms.ModelForm):

    class Meta:
        model = Images
        images = forms.ImageField()

        fields = ('images',)

        widgets = {'images': forms.ClearableFileInput(attrs={
            'type': 'file',
            'class': 'custom-file-input',
            'id': 'inputGroupImage',
            'multiple': True,
            'label': 'Image',
            'debug': 'multiple files form',
        }), }


class FilesForm(forms.ModelForm):

    class Meta:
        model = Files
        files = forms.FileField()
        fields = ('files',)
        widgets = {'files': forms.ClearableFileInput(attrs={
            'type': 'file',
            'class': 'custom-file-input',
            'id': 'inputGroupFile',
            'multiple': True,
            'label': 'File',
            'debug': 'multiple files form',
        }), }


class PostLikeDislikeMeme(forms.ModelForm):

    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    class Meta:
        model = MemesUsersLikes
        like = forms.IntegerField(max_value=1, min_value=-1)
        fields = ('like', )
        widgets = {
            'like': forms.IntegerField()
        }


# class PostFormMeme(forms.Form):
#     title = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 'type': 'text', 'aria-label': 'Post_title',
#         'aria-describedby': 'inputGroup-sizing-default'}),
#         max_length=255,
#     )
#     tags = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control', 'type': 'text', 'aria-label': 'Post_tags',
#         'aria-describedby': 'inputGroup-sizing-default'}),
#         max_length=255,
#     )
#     # TODO: Specify only for user membership
#     tubes = ModelChoiceField(
#         queryset=MemesTubes.objects.all(),
#         to_field_name="tube",
#         empty_label="(Nothing)",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     # upload_to='documents/'
#     image = forms.FileField(widget=forms.ClearableFileInput(attrs={
#         'type': 'file',
#         'class': 'custom-file-input',
#         'id': 'inputGroupImage',
#         'multiple': True,
#
#     }))
#     # upload_to='documents/'
#     file = forms.FileField(widget=forms.ClearableFileInput(attrs={
#         'type': 'file',
#         'class': 'custom-file-input',
#         'id': 'inputGroupFile',
#         'multiple': True,
#     }))
#
#     link = forms.URLField(widget=forms.URLInput(attrs={
#         'class': 'form-control', 'type': 'text', 'aria-label': 'Small',
#         'aria-describedby': 'inputGroup-sizing-sm'}),
#         max_length=255,
#     )
#
#     text = forms.CharField(widget=forms.Textarea(attrs={
#         'test': 'its working!', 'class': 'form-control', 'aria-label': 'Short post', 'rows': '4', 'cols': '4'}),
#         max_length=600,
#     )
#
#     hypertext = forms.CharField(widget=forms.Textarea(attrs={
#         'test': 'its working!', 'class': 'form-control', 'aria-label': 'Long post', 'rows': '20', 'cols': '4'}),
#         max_length=6500,
#     )

