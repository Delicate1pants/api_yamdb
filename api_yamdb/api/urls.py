from django.urls import include, path
from rest_framework import routers

from .views import RegistrationAPIView, AuthenticationAPIView, UserViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', AuthenticationAPIView.as_view()),
]
