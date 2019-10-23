import datetime

from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.forms import modelformset_factory

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from core.user_operations import UserCheck
from core.models import AuthUser
from memes.models import MemesObject, Images, Files, MemesTubes
from memes.db_oper import Selections

from memes.forms import PostFormMeme, ImagesForm, FilesForm, PostLikeDislikeMeme, TubeCreateForm
from memes.api.serializers import MemesObjectSerializer

# Python logger
import logging

log = logging.getLogger("core.corelogger")


class Memes:

    @staticmethod
    def public(request):
        page_widgets = loader.get_template('root/memes/memes_main.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> public(): %s", user_string)
        debug = request.GET.get('debug', False)
        page = request.GET.get('page', 1)

        # Display only public tubes:
        pub_tubes = MemesTubes.objects.filter(is_private__exact=False)
        log.debug("Pub tubes: %s", pub_tubes)
        pub_memes = MemesObject.objects.filter(tubes__in=pub_tubes).order_by('-pub_date')

        log.debug("Public memes: %s", pub_memes)

        # Paginator:
        memes_p = Paginator(pub_memes, 10)
        try:
            memes_pages = memes_p.page(page)
        except PageNotAnInteger:
            memes_pages = memes_p.page(1)
        except EmptyPage:
            memes_pages = memes_p.page(memes_p.num_pages)

        widgets = dict(
            SUBJECT="All public visible memes!",
            MEMES=memes_pages,
            page=page,
            DEBUG=debug,
            # MEME_JSON=MemesObjectSerializer(all_memes, many=False, context={'request': request}),
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def my_tubes(request):
        page_widgets = loader.get_template('root/memes/memes_main.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> my_tubes(): %s", user_string)
        debug = request.GET.get('debug', False)

        tube_admin = request.GET.get('tube_admin')
        public = request.GET.get('public')
        private = request.GET.get('private')
        page = request.GET.get('page', 1)

        auth_user = AuthUser.objects.get(username=request.user)
        # Display only tubes where user is admin:
        if tube_admin:
            my_admin_tubes = MemesTubes.objects.filter(tube_admin=auth_user)
            my_tubes = my_admin_tubes
            subject = "All memes from tubes where I'm a Admin!"
        # Display only tubes where user is member:
        else:
            my_tubes = MemesTubes.objects.filter(tube_members=auth_user)
            subject = "All memes from tubes where I'm a member!"

        if private:
            my_tubes = my_tubes.filter(is_private__exact=True)
            subject = "All memes from tubes where I'm a member only private!"

        my_tube_memes = MemesObject.objects.filter(tubes__in=my_tubes)

        # Also include public tubes
        if public:
            pub_tubes = MemesTubes.objects.filter(is_private__exact=False)
            pub_memes = MemesObject.objects.filter(tubes__in=pub_tubes)
            my_tube_memes = my_tube_memes | pub_memes
            subject = "All memes from tubes where I'm a member + private AND all Public tubes!"

        log.debug("My tubes memes: %s", my_tube_memes)

        # Paginator:
        memes_p = Paginator(my_tube_memes.order_by('-pub_date'), 10)
        try:
            memes_pages = memes_p.page(page)
        except PageNotAnInteger:
            memes_pages = memes_p.page(1)
        except EmptyPage:
            memes_pages = memes_p.page(memes_p.num_pages)

        widgets = dict(
            DEBUG=debug,
            SUBJECT=subject,
            MEMES=memes_pages,
            private=private,
            public=public,
            page=page,
            # MEME_JSON=MemesObjectSerializer(my_tube_memes, many=False, context={'request': request}),
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    def single_tube(request):
        page_widgets = loader.get_template('root/memes/memes_main.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> single_tube(): %s", user_string)
        debug = request.GET.get('debug', False)

        page = request.GET.get('page', 1)
        tube_id = request.GET.get('tube_id')
        tube_obj = MemesTubes.objects.filter(id=tube_id)

        if tube_obj[0].is_private:
            log.info("This is a private tube: %s - %s", tube_obj[0].is_private, tube_obj)
            if request.user.is_authenticated:
                auth_user = AuthUser.objects.get(username=user_name)
                is_admin = tube_obj.filter(tube_admin=auth_user)
                # log.debug("is_admin: %s", is_admin)
                is_member = tube_obj.filter(tube_members=auth_user)
                # log.debug("is_member: %s", is_member)
                if not is_admin and not is_member:
                    log.warning("<=single_tube=> Current user is not a member nor admin of this private tube. "
                                "Redirecting to public tubes instead.")
                    return redirect('/memes/public/')
                else:
                    # Let use see his private memes if he is an admin or member of this tube.
                    pass
            else:
                log.info("<=single_tube=> Cannot check Anon - is_admin/is_member for private tube - "
                         "redirecting to public memes!")
                return redirect('/memes/public/')
        else:
            # Tube is not private - show all memes to everyone!
            pass

        subject = "All memes from only selected tube!"
        all_memes = MemesObject.objects.filter(tubes__in=tube_obj).order_by('-pub_date')
        log.debug("Single tube memes: %s", all_memes)

        # Paginator:
        memes_p = Paginator(all_memes.order_by('-pub_date'), 10)
        try:
            memes_pages = memes_p.page(page)
        except PageNotAnInteger:
            memes_pages = memes_p.page(1)
        except EmptyPage:
            memes_pages = memes_p.page(memes_p.num_pages)

        widgets = dict(
            DEBUG=debug,
            SUBJECT=subject,
            MEMES=memes_pages,
            tube_id=tube_id,
            page=page,
            # MEME_JSON=MemesObjectSerializer(all_memes, many=False, context={'request': request}),
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    def meme(request, meme_id=None):
        """
        Serialize meme object tp JSON and pass to JS + ajax operations:
        - https://stackoverflow.com/a/28750126/4915733
        - https://stackoverflow.com/a/8483184/4915733

        :param request:
        :return:
        """
        page_widgets = loader.get_template('root/memes/widgets/single_meme.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> meme(): %s", user_string)
        debug = request.GET.get('debug', False)

        if not meme_id:
            log.debug("<=Memes Widgets=> No meme id in args use context!")
            meme_id = request.GET.get('meme')
        is_author = False
        is_admin = False
        is_member = False
        log.debug("<=Memes Widgets=> meme_id(): %s", meme_id)

        try:
            meme_obj = MemesObject.objects.get(id=meme_id)
        except ObjectDoesNotExist:
            return HttpResponse(status=404)

        if meme_obj:
            current_meme_tube = MemesTubes.objects.filter(memesobject=meme_obj)
            log.debug("current_meme_tube: %s", current_meme_tube)

            if request.user.is_authenticated:
                auth_user = AuthUser.objects.get(username=user_name)
                is_admin = current_meme_tube.get(tube_admin=auth_user)
                # log.debug("is_admin: %s", is_admin)

                if current_meme_tube and current_meme_tube[0].is_private:
                    is_member = current_meme_tube.get(tube_members=auth_user)
                    log.debug("is_member: %s", is_member)
                    if not is_admin and not is_member:
                        # subject = "You're trying to pick a forbidden fruit, please step back and stop trying to!"
                        return redirect('/memes/public/')

                meme = meme_obj
                log.debug("Single meme: %s", meme_obj)

                if meme_obj.author == auth_user:
                    is_author = True
            else:
                # Show just if public tube meme
                if current_meme_tube and current_meme_tube[0].is_private:
                    subject = 'No such meme found!'
                    return redirect('/memes/public/')
                else:
                    meme = meme_obj

            subject = "Check this meme, leave a comment or check who liked or disliked it, whatever!"

            widgets = dict(
                DEBUG=debug,
                SUBJECT=subject,
                MEME=meme,
                # https://stackoverflow.com/a/28750126/4915733
                MEME_JSON=MemesObjectSerializer(meme, many=False, context={'request': request}),
                user_name=user_name,
                IS_AUTHOR=is_author,
                IS_ADMIN=is_admin,
            )
            return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def post_meme(request):
        """
        Multiple images in one post: https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django

        :param request:
        :return:
        """
        page_widgets = loader.get_template('root/memes/widgets/post_meme.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> meme(): %s", user_string)
        debug = request.GET.get('debug', False)

        picture = request.GET.get('picture')
        file = request.GET.get('file')
        short_text = request.GET.get('short_text')
        hypertext = request.GET.get('hypertext')
        link = request.GET.get('link')
        # Not really a useful type of post
        meme_set = request.GET.get('meme_set')
        is_author = True

        auth_user = AuthUser.objects.get(username=user_name)

        if request.method == 'POST':
            # form = PostFormMeme(request.POST, request.FILES)
            form = PostFormMeme(auth_user, request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)
                post.author = auth_user

                # if request.FILES.get('image', False):
                #     image = request.FILES['image']
                #     log.debug("image: %s", request.FILES.get('image', []))
                #
                # if request.FILES.get('file', False):
                #     files = request.FILES['file']
                #     log.debug("Request get files: %s", files)
                #     # for file in files:
                #     #     file_name = fs_files.save(file.name, file)
                #     #     log.debug("Saving file_name: %s", file_name)

                post.save()
                return redirect('meme_posted', meme_id=post.id)
        else:
            form = PostFormMeme(auth_user)
            widgets = dict(
                DEBUG=debug,
                SUBJECT="Post a meme!",
                PICTURE=picture,
                FILE=file,
                LINK=link,
                SHORT_TEXT=short_text,
                HYPERTEXT=hypertext,
                # Not really a useful type of post
                MEME_SET=meme_set,
                form=form,
            )
            return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def delete_single_meme(request):
        page_widgets = loader.get_template('root/memes/widgets/single_meme.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> meme(): %s", user_string)
        debug = request.GET.get('debug', False)

        auth_user = AuthUser.objects.get(username=request.user)

        meme_id = request.GET.get('meme_id')
        try:
            meme_obj = MemesObject.objects.get(id=meme_id, author=auth_user)
        except ObjectDoesNotExist:
            meme_obj = False

        if meme_obj:
            subject = "Meme has been deleted!"
            meme_obj.delete()
        else:
            subject = "Meme cannot be deleted! You're probably not an author, or this meme id does not exists!"

        return redirect('/memes/public/')

    # DEV
    @staticmethod
    @login_required(login_url='/accounts/login/')
    def post_multiple(request):
        """
        Multiple images in one post: https://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django

        :param request:
        :return:
        """
        page_widgets = loader.get_template('root/memes/widgets/post_meme.html')
        posted_meme = loader.get_template('root/memes/widgets/single_meme.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=Memes Widgets=> meme(): %s", user_string)

        images_form_set = modelformset_factory(Images, form=ImagesForm, extra=10)
        files_form_set = modelformset_factory(Files, form=FilesForm, extra=10)

        if request.method == 'POST':
            # form = PostFormMeme(request.POST, request.FILES)
            form = PostFormMeme(request.POST)
            images_formset = images_form_set(request.POST, request.FILES, queryset=Images.objects.none())
            files_formset = files_form_set(request.POST, request.FILES, queryset=Files.objects.none())

            if form.is_valid() and images_formset.is_valid() and files_formset.is_valid():
                log.debug("form: %s", form)
                post = form.save(commit=False)
                auth_user = AuthUser.objects.get(username=request.user)
                log.debug("request.user: %s", request.user)
                log.debug("auth_user: %s", auth_user)
                post.author = auth_user

                log.debug("request.FILES %s", request.FILES)
                for form in images_form_set.cleaned_data:
                    if form:
                        image = form['image']
                        photo = Images(post=post, image=image)
                        photo.save()

                for form in files_form_set.cleaned_data:
                    if form:
                        image = form['image']
                        photo = Images(post=post, image=image)
                        photo.save()

                # if request.FILES.get('image', False):
                #     image = request.FILES['image']
                #     log.debug("image: %s", request.FILES.get('image', []))
                #     image_name = fs_images.save(image.name, image)
                #     log.debug("image_name: %s", image_name)
                #     # log.debug("Request get images: %s", images)
                #     # for image in images:
                #     #     log.debug("Saving image_name: %s", image_name)
                # if request.FILES.get('file', False):
                #     files = request.FILES['file']
                #     log.debug("Request get files: %s", files)
                #     for file in files:
                #         file_name = fs_files.save(file.name, file)
                #         log.debug("Saving file_name: %s", file_name)

                post.save()

                meme_obj = MemesObject.objects.get(id=post.id)
                widgets = dict(SUBJECT="You posted this!", MEME=meme_obj)
                return HttpResponse(posted_meme.render(widgets, request))
        else:
            form = PostFormMeme()
            images_formset = images_form_set(queryset=Images.objects.none())
            files_formset = files_form_set(queryset=Files.objects.none())
            widgets = dict(
                form=form,
                images_formset=images_formset,
                files_formset=files_formset,
            )
            return HttpResponse(page_widgets.render(widgets, request))


class UserSpace:

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def space(request):
        page_widgets = loader.get_template('root/user_space/user_space_main.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=User Space=> public(): %s", user_string)

        my_memes = request.GET.get('my_memes')
        page = request.GET.get('page', 1)

        auth_user = AuthUser.objects.get(username=user_name)
        tubes_admin = MemesTubes.objects.filter(tube_admin=auth_user)
        tubes_member = MemesTubes.objects.filter(tube_members=auth_user)

        if my_memes == 'my_memes':
            memes_items = MemesObject.objects.filter(author=auth_user)
        elif my_memes == 'my_best':
            memes_items = MemesObject.objects.filter(author=auth_user)
        else:
            memes_items = MemesObject.objects.filter(author=auth_user)

        widgets = dict(
            SUBJECT="User space",
            my_memes=my_memes,
            auth_user=auth_user,
            tubes_admin=tubes_admin,
            tubes_member=tubes_member,
            memes_items=memes_items.order_by('-pub_date'),
        )
        return HttpResponse(page_widgets.render(widgets, request))


class TubeViews:

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def list_tubes(request):
        page_widgets = loader.get_template('root/tubes_space/tubes_main.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> list(): %s", user_string)

        tubes_mode = request.GET.get('tubes_mode')
        page = request.GET.get('page', 1)

        auth_user = AuthUser.objects.get(username=user_name)

        if tubes_mode == 'popular':
            subject = 'All popular tubes of all times (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'all':
            subject = 'All tubes of all times'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'recommended':
            subject = 'Our recommendations (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'best':
            subject = 'Best tubes by rating of all times (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'today':
            subject = 'Best tubes by rating today (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'growing':
            subject = 'Best tubes by rating of newly created (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        elif tubes_mode == 'user_admin':
            subject = 'All tubes where you are an admin!'
            tubes = MemesTubes.objects.filter(tube_admin=auth_user)

        elif tubes_mode == 'user_member':
            subject = 'All tubes where you are a member!'
            tubes = MemesTubes.objects.filter(is_private__exact=False,
                                              tube_members=auth_user)

        elif tubes_mode == 'user_private':
            subject = 'All private tubes where you are a member!'
            tubes = MemesTubes.objects.filter(is_private__exact=True,
                                              tube_members=auth_user)

        else:
            subject = 'Not set - show everything (in progress...)'
            tubes = MemesTubes.objects.filter(is_private__exact=False)

        widgets = dict(
            SUBJECT=subject,
            auth_user=auth_user,
            tubes_mode=tubes_mode,
            QUERYSET=tubes,
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def manage(request):
        page_widgets = loader.get_template('root/tubes_space/tube_manage.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> manage(): %s", user_string)

        tube_id = request.GET.get('tube_id')
        tube_join = request.GET.get('tube_join')
        tube_leave = request.GET.get('tube_leave')

        tube_admin = False
        tube_member = False

        tube = MemesTubes.objects.get(id=tube_id)
        auth_user = AuthUser.objects.get(username=user_name)

        log.warning("Tube attrs: tube.is_private %s", tube.is_private)

        # If current user is a member of this PRIVATE tube?
        if tube.is_private:
            if auth_user not in tube.tube_members.all():
                log.warning("User tries to manage private tube where he is not member! %s", tube)
                return redirect('tubes')

        # If current user is an admin of this tube?
        if tube.tube_admin == auth_user:
            log.warning("User is an admin of current tube! %s", tube)
            tube_admin = True

        # If current user is a member of this tube?
        log.warning("tube.tube_members! %s", tube.tube_members)
        if auth_user in tube.tube_members.all():
            log.warning("User is a member of current tube! %s", tube)
            tube_member = True

        widgets = dict(
            SUBJECT="Manage the tube! You can see members, manage them if you're admin or change "
                    "public status of this tube, change admin role or delete tube!",
            tube=tube,
            auth_user=auth_user,
            tube_admin=tube_admin,
            tube_member=tube_member,
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def create(request):
        page_widgets = loader.get_template('root/tubes_space/tube_create.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> create(): %s", user_string)

        tube_create = request.GET.get('tube_create', False)

        auth_user = AuthUser.objects.get(username=user_name)

        tube_f = TubeCreateForm(request.POST or None)
        if request.method == 'POST':
            if tube_f.is_valid():
                tube_p = tube_f.save(commit=False)
                tube_p.tube_admin = auth_user
                tube_p.save()
                tube_p.tube_members.add(auth_user)
                return HttpResponseRedirect('/memes/tubes/?tubes_mode=user_admin')
            # else:
            #     messages.error(request, "Error")
            #     log.error("For is invalid - return something: %s", tube_f)
        widgets = dict(SUBJECT="Create a tube!", form=tube_f)
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def leave(request):
        page_widgets = loader.get_template('root/tubes_space/tube_join.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> leave(): %s", user_string)

        tube_id = request.GET.get('tube_id')
        to_leave = request.GET.get('to_leave', False)

        tube = MemesTubes.objects.get(id=tube_id)
        auth_user = AuthUser.objects.get(username=user_name)

        # If current user is a member of this PRIVATE tube?
        if tube.is_private:
            if auth_user not in tube.tube_members.all():
                log.warning("User tries to manage private tube where he is not member! %s", tube)
                return redirect('tubes')

        if auth_user in tube.tube_members.all():
            log.info("User is a member of current tube! %s", tube)

        if to_leave:
            tube.tube_members.remove(auth_user)
            subject = "You have leaved this tube!"
        else:
            subject = "Do you want to leave this tube?"

        tube_memes = MemesObject.objects.filter(tubes=tube)

        widgets = dict(
            SUBJECT=subject,
            tube=tube,
            auth_user=auth_user,
            tube_memes=tube_memes,
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def join(request):
        page_widgets = loader.get_template('root/tubes_space/tube_join.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> join(): %s", user_string)

        tube_id = request.GET.get('tube_id')
        to_join = request.GET.get('to_join', False)

        tube = MemesTubes.objects.get(id=tube_id)
        auth_user = AuthUser.objects.get(username=user_name)

        # If current user is a member of this PRIVATE tube?
        if tube.is_private:
            if auth_user not in tube.tube_members.all():
                log.warning("User tries to manage private tube where he is not member! %s", tube)
                return redirect('tubes')

        if auth_user in tube.tube_members.all():
            log.info("User is a member of current tube! %s", tube)

        if to_join:
            tube.tube_members.add(auth_user)
            subject = "You have joined this tube!"
        else:
            subject = "Do you want to join this tube?"

        tube_memes = MemesObject.objects.filter(tubes=tube)

        widgets = dict(
            SUBJECT=subject,
            auth_user=auth_user,
            tube=tube,
            tube_memes=tube_memes,
        )
        return HttpResponse(page_widgets.render(widgets, request))

    @staticmethod
    @login_required(login_url='/accounts/login/')
    def delete(request):
        page_widgets = loader.get_template('root/tubes_space/tube_join.html')
        user_name, user_string = UserCheck().user_string_f(request)
        log.debug("<=TubeViews=> leave(): %s", user_string)

        tube_id = request.GET.get('tube_id')

        tube = MemesTubes.objects.get(id=tube_id)
        auth_user = AuthUser.objects.get(username=user_name)

        # If current user is an admin of this tube?
        if tube.tube_admin == auth_user:
            tube_admin = True
            log.warning("<=delete=> User is an admin of current tube! %s", tube)
            subject = 'Tube have been deleted!'
            tube.delete()
            return HttpResponseRedirect('/memes/tubes/?tubes_mode=user_admin')
        else:
            return HttpResponseRedirect('/memes/tubes/?tubes_mode=user_admin')