from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.models import AuthUser

from memes import services
from memes.models import MemesObject, MemesUsersComments, MemesUsersLikes, MemesTubes
from memes.api.serializers import MemesObjectSerializer, MemesUsersCommentsSerializer, \
    MemesUsersLikesSerializer, MemesTubesSerializer, MemesAuthorSerializer
from memes.api.mixins import LikedMixin, CommentMixin, TubesMixin

import logging
log = logging.getLogger("core.corelogger")


class MemesObjectViewSet(LikedMixin, CommentMixin, viewsets.ModelViewSet):
    """
    Memes - in addition collects all likes, dislikes, comments.
    """
    log.debug("MemesObjectViewSet meme!")
    queryset = MemesObject.objects.all().order_by('-pub_date')
    serializer_class = MemesObjectSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class MemesUsersCommentsViewSet(viewsets.ModelViewSet):
    """
    Comments
    https://stackoverflow.com/questions/38670510/how-to-add-comment-box-and-post-form-to-django-rest-framework
    """
    queryset = MemesUsersComments.objects.all().order_by('-pub_date')
    serializer_class = MemesUsersCommentsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class MemesUsersLikesViewSet(viewsets.ModelViewSet):
    """
    Likes
    """
    queryset = MemesUsersLikes.objects.all().order_by('-pub_date')
    serializer_class = MemesUsersLikesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class MemesTubesViewSet(TubesMixin, viewsets.ModelViewSet):

    model = MemesTubes
    serializer_class = MemesTubesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        user_author = AuthUser.objects.get(id=self.request.user.id)
        # log.debug("<MemesTubesViewSet=> get_queryset - > user_author: %s", user_author)
        queryset = MemesTubes.objects.filter(
            is_private__exact=False
        ).distinct() | MemesTubes.objects.filter(
            tube_admin=user_author
        ).distinct() | MemesTubes.objects.filter(
            tube_members=user_author
        ).distinct()
        # log.debug("<MemesTubesViewSet=> get_queryset - > queryset query: %s", queryset.query)
        return queryset

    # def list(self, request):
    #     # obj = self.get_object()
    #     # log.debug("<=MemesTubesViewSet=> list -> obj: %s", obj)
    #     log.debug("<=MemesTubesViewSet=> list request.user: %s", request.user)
    #     user_author = AuthUser.objects.get(id=request.user.id)
    #     queryset = MemesTubes.objects.filter(
    #         is_private__exact=False,
    #     ) | MemesTubes.objects.filter(
    #         tube_admin=user_author
    #     ) | MemesTubes.objects.filter(
    #         tube_members=user_author
    #     )
    #     serializer = self.serializer_class(queryset, many=True)
    #
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     # obj = self.get_object()
    #     # log.debug("<=MemesTubesViewSet=> retrieve -> obj: %s", obj)
    #     log.debug("<=MemesTubesViewSet=> retrieve request.user: %s", request.user)
    #     user_author = AuthUser.objects.get(id=request.user.id)
    #     queryset = MemesTubes.objects.filter(
    #         id=pk, tube_admin=user_author
    #     ) | MemesTubes.objects.filter(
    #         id=pk, tube_members=user_author
    #     ) | MemesTubes.objects.filter(
    #         id=pk, is_private__exact=False
    #     )
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)
    # @action(detail=True, methods=['POST'])
    # def join_tube(self, request, pk=None):
    #     log.debug("<=MemesTubesViewSet=> pk: %s", pk)
    #     log.debug("<=MemesTubesViewSet=> self: %s", self)
    #
    #     get_object = self.get_object()
    #     log.debug("<=MemesTubesViewSet=> join_tube -> obj: %s", get_object)
    #     # get_queryset = self.get_queryset()
    #     # log.debug("<=MemesTubesViewSet=> join_tube -> get_queryset: %s", get_queryset)
    #
    #     log.debug("<=MemesTubesViewSet=> join_tube -> request.user: %s", request.user)
    #     members = services.TubeActions.join_public_tube(get_object, request.user)
    #     log.debug("<=MemesTubesViewSet=> join_tube -> members: %s", members)
    #     serializer = MemesAuthorSerializer(members, many=True)
    #     return Response({'action': 'joined', 'members': serializer.data})


class MemesAuthorViewSet(viewsets.ModelViewSet):
    """
    Tubes
    """
    queryset = AuthUser.objects.all().order_by('id')
    serializer_class = MemesAuthorSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
