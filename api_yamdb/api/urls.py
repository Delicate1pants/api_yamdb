from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (AuthenticationAPIView, CategoryViewSet, CommentViewSet,
                    GenreViewSet, RegistrationAPIView, ReviewViewSet,
                    TitlesViewSet, UserDetail, UserList)

router = routers.SimpleRouter()
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', AuthenticationAPIView.as_view()),
    path('v1/users/', UserList.as_view()),
    path('v1/users/<str:username>/', UserDetail.as_view()),
    path('v1/auth/token-verify', TokenVerifyView.as_view()),
]
