from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework_jwt.settings import api_settings

from user.models import SysUser, SysUserSerializer


class LoginView(View):
    def post(self, request):
        username = request.GET.get('username')
        password = request.GET.get('password')
        try:
            user = SysUser.objects.get(username=username, password=password)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
        except Exception as e:
            return JsonResponse({'code': 500, 'info': '账号或密码错误'})
        return JsonResponse({'code': 200, 'user': SysUserSerializer(user).data, 'token': token, 'info': 'OK'})


# Create your views here.
class TestView(View):

    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token != None and token != '':
            UserList_queryset = SysUser.objects.all()
            UserList_dic = UserList_queryset.values()
            UserList = list(UserList_dic)
            return JsonResponse({"code": 200, "UserList": UserList})
        else:
            return JsonResponse({'code': 401, 'info': '没有访问权限！'})


class JwtTestView(View):

    def get(self, request):
        user = SysUser.objects.get(username='python222')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return JsonResponse({'code': 200, 'token': token})
