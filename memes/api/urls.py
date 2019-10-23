
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter
from memes.api.viewsets import MemesObjectViewSet, \
    MemesUsersCommentsViewSet, MemesUsersLikesViewSet, MemesTubesViewSet, MemesAuthorViewSet


# https://apirobot.me/posts/how-to-implement-liking-in-django
# Создаем router и регистрируем ViewSet
router = DefaultRouter()
router.register(r'memes', MemesObjectViewSet)
router.register(r'comments', MemesUsersCommentsViewSet)
router.register(r'likes', MemesUsersLikesViewSet)
router.register(r'authors', MemesAuthorViewSet)

router.register(r'tubes', MemesTubesViewSet, basename='tubes')

# URLs настраиваются автоматически роутером
# urlpatterns = router.urls
urlpatterns = [
    url(r'^', include(router.urls)),
]