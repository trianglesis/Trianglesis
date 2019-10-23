
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from memes import services
from memes.api.serializers import MemesUsersLikesSerializer, MemesUsersCommentsSerializer, MemesAuthorSerializer

import logging
log = logging.getLogger("core.corelogger")


class LikedMixin:

    @detail_route(methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        services.Likes.like_meme(obj, request.user)
        likes = services.Likes.all_likes(obj)
        return Response({'likes': len(likes)})

    @detail_route(methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        services.Likes.remove_like_meme(obj, request.user)
        return Response()

    @detail_route(methods=['GET'])
    def likes(self, request, pk=None):
        obj = self.get_object()
        likes = services.Likes.all_likes(obj)
        serializer = MemesUsersLikesSerializer(likes, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def liking(self, request, pk=None):
        obj = self.get_object()
        action = services.Likes().liking(obj, request.user)
        likes = services.Likes.all_likes(obj)
        serializer = MemesUsersLikesSerializer(likes, many=True)
        return Response({'likes': len(likes), 'action': action, 'likers': serializer.data})

    @detail_route(methods=['POST'])
    def dislike(self, request, pk=None):
        obj = self.get_object()
        services.Dislikes.dislike_meme(obj, request.user)
        dislikes = services.Dislikes.all_dislikes(obj)
        return Response({'dislikes': len(dislikes)})

    @detail_route(methods=['POST'])
    def undislike(self, request, pk=None):
        obj = self.get_object()
        services.Dislikes.remove_dislike_meme(obj, request.user)
        return Response()

    @detail_route(methods=['GET'])
    def dislikes(self, request, pk=None):
        obj = self.get_object()
        dislikes = services.Dislikes.all_dislikes(obj)
        serializer = MemesUsersLikesSerializer(dislikes, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST'])
    def disliking(self, request, pk=None):
        obj = self.get_object()
        action = services.Dislikes().disliking(obj, request.user)
        dislikes = services.Dislikes.all_dislikes(obj)
        serializer = MemesUsersLikesSerializer(dislikes, many=True)
        return Response({'dislikes': len(dislikes), 'action': action, 'dislikers': serializer.data})


class CommentMixin:

    @detail_route(methods=['POST'])
    def comment(self, request, pk=None):
        obj = self.get_object()
        services.Comments.leave_comment(obj, request.user, comment=request.GET.get('comment'))
        return Response()

    @detail_route(methods=['POST'])
    def comment_delete(self, request, pk=None):
        obj = self.get_object()
        services.Comments.delete_comment(obj, request.user)
        return Response()

    @detail_route(methods=['GET'])
    def comments(self, request, pk=None):
        log.debug("comments -> request: %s", request)

        obj = self.get_object()
        comments = services.Comments.get_all_comments(obj)
        serializer = MemesUsersCommentsSerializer(comments, many=True)
        return Response(serializer.data)


class TubesMixin:

    @detail_route(methods=['POST'])
    def join_tube(self, request, pk=None):
        log.debug("<=TubesMixin=> pk: %s", pk)
        log.debug("<=TubesMixin=> self: %s", self)
        obj = self.get_object()
        log.debug("<=TubesMixin=> join_tube -> obj: %s", obj)
        log.debug("<=TubesMixin=> join_tube -> request.user: %s", request.user)
        members = services.TubeActions.join_public_tube(obj, request.user)
        log.debug("<=TubesMixin=> join_tube -> members: %s", members)
        serializer = MemesAuthorSerializer(members, many=True)
        return Response({'action': 'joined', 'members': serializer.data})

    @detail_route(methods=['POST'])
    def leave_tube(self, request, pk=None):
        obj = self.get_object()
        log.debug("<=TubesMixin=> join_tube -> obj: %s", obj)
        log.debug("<=TubesMixin=> join_tube -> request.user: %s", request.user)
        members = services.TubeActions.leave_tube(obj, request.user)
        log.debug("<=TubesMixin=> join_tube -> members: %s", members)
        serializer = MemesAuthorSerializer(members, many=True)
        return Response({'action': 'leaved', 'members': serializer.data})

    @detail_route(methods=['POST'])
    def change_admin(self, request, pk=None):
        obj = self.get_object()
        # Assign admin role of this tube to another user
        pass

    @detail_route(methods=['POST'])
    def add_member(self, request, pk=None):
        obj = self.get_object()
        # Only if user is admin - can add any member to private (not public?)
        pass

    @detail_route(methods=['POST'])
    def remove_member(self, request, pk=None):
        obj = self.get_object()
        # Remove member only if user is admin
        pass
