from django.urls import path

from user.views import TestView, JwtTestView, LoginView, UserInfoUpdateView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path("test", TestView.as_view(), name='test'),
    path("jwt_test", JwtTestView.as_view(), name='jwt_test'),
    path("update", UserInfoUpdateView.as_view(), name='user_update'),
]
