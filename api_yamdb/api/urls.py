from django.urls import include, path

from rest_framework import routers

from .views import CategoryViewSet, GenreViewSet, TitlesViewSet

router_v1 = routers.DefaultRouter()

router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'titles', TitlesViewSet, basename='titles')

v1_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('', include(router_v1.urls)),
]

urlpatterns = [
    path('v1/', include(v1_patterns)),
]