import datetime

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_jwt.settings import api_settings
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError


class JwtAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        white_list = ['/user/login']  # 白名单
        path = request.path
        if request.path not in white_list and not path.startswith('/media'):
            token = request.META.get("HTTP_AUTHORIZATION")
            print("token:" + str(token))
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                payload = jwt_decode_handler(token)
                exp_time = datetime.datetime.fromtimestamp(payload['exp'])
            except ExpiredSignatureError:
                return HttpResponse("token已过期，请重新登录")
            except InvalidTokenError:
                return HttpResponse("token验证失败")
            except PyJWTError:
                return HttpResponse("token验证异常")
            print('需要token验证')
        else:
            print("不需要token验证")
            return None
