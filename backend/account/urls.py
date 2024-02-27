from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from django.views.generic import RedirectView
from account.views.UserView import *
from account.views.user import UserView,GetUserView
from rest_framework import routers


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'', UserSuggestView, basename='suggest-user')
router.register(r'user', UserView, basename='user')


urlpatterns = [
  #  path("", RedirectView.as_view(url="login/", permanent=False)),
    path("register", RegisterView.as_view(), name="register"),
    path("token/refresh", TokenRefreshView.as_view(), name='token_refresh'),
    path("login", LoginView.as_view(), name="login"),
    path("change-password", ChangePasswordView.as_view(), name="change-password"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path('',include(router.urls)),
    path('user/<int:pk>',GetUserView.as_view()),
    path('admin/account',AccountAdmin.as_view()),
    path('admin/account/<int:pk>',AccountDetailAdmin.as_view()),


]
