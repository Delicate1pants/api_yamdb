from django.urls import include, path

from .views import RegistrationAPIView, AuthenticationAPIView
#from rest_framework import routers
from rest_framework_simplejwt.views import TokenVerifyView

from . import views
from .views import UserList, UserDetail

app_name = 'api'

#router = routers.DefaultRouter()
#router.register('users', UserViewSet, basename='users')

urlpatterns = [
    #path('v1/', include(router.urls)),
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', AuthenticationAPIView.as_view()),
    path('v1/users/', UserList.as_view()),
    path('v1/users/<str:username>/', UserDetail.as_view()),
    path('v1/auth/token-verify/', TokenVerifyView.as_view()),
]