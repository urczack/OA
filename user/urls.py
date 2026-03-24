from django.urls import path

from user.views import TestView, JwtTestView, LoginView, UserInfoUpdateView, PwdModifyView, ImageView, AvatarView, \
    SearchView

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path("test", TestView.as_view(), name='test'),
    path("jwt_test", JwtTestView.as_view(), name='jwt_test'),
    path("update", UserInfoUpdateView.as_view(), name='user_update'),
    path("pwd_modify", PwdModifyView.as_view(), name='pwd_modify'),
    path('uploadImage', ImageView.as_view(), name='uploadImage'),  # 头像上传
    path('updateAvatar', AvatarView.as_view(), name='updateAvatar'),  # 更新头像
    path('search', SearchView.as_view(), name="search"),
]
