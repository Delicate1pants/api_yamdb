from django.urls import include, path

from .views import RegistrationAPIView, AuthenticationAPIView, UserViewSet
from rest_framework import routers


from .views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', AuthenticationAPIView.as_view()),
]