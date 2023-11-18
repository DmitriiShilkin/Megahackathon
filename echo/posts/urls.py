from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, CategoryViewSet, ReviewViewSet, CommentViewSet, VoteViewSet

router = routers.DefaultRouter()

router.register('posts', PostViewSet, basename='post')
router.register('categories', CategoryViewSet, basename='category')
router.register('reviews', ReviewViewSet, basename='review')
router.register('comments', CommentViewSet, basename='comment')
router.register('votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
