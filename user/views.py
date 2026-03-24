from django.core import paginator
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework_jwt.settings import api_settings

from OA import settings
from menu.models import SysMenu, SysMenuSerializer
from role.models import SysRole
from user.models import SysUser, SysUserSerializer
import json
import datetime


class LoginView(View):

    def biuldTreeMenu(self, sysMenuList):
        resultMenuList: list[SysMenu] = list()
        for menu in sysMenuList:
            # 寻找子节点
            for e in sysMenuList:
                if e.parent_id == menu.id:
                    if not hasattr(menu, 'children'):
                        menu.children = list()
                    menu.children.append(e)
            # 寻找父节点
            if menu.parent_id == 0:
                resultMenuList.append(menu)
        return resultMenuList

    def post(self, request):
        # username = request.GET.get('username')
        # password = request.GET.get('password')
        data = json.loads(request.body.decode("utf-8"))
        username = data['username']
        password = data['password']
        print(username, password)
        try:
            user = SysUser.objects.get(username=username, password=password)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            roleList = SysRole.objects.raw(
                "SELECT id,name from sys_role where id in (SELECT role_id from sys_user_role where user_id = " + str(
                    user.id) + ")")
            # print(roleList)
            MenuSet: set[SysMenu] = set()
            for row in roleList:
                menuList = SysMenu.objects.raw(
                    "select * from sys_menu where id in (SELECT menu_id from sys_role_menu where role_id =" + str(
                        row.id) + " )")
                for row2 in menuList:
                    # print(row2.id, row2.name)
                    MenuSet.add(row2)
            MenuList: list[SysMenu] = list(MenuSet)  # set转list
            sorted_menuList = sorted(MenuList)  # 排序
            # print(sorted_menuList)
            # 构造菜单树
            sysMenuList: list[SysMenu] = self.biuldTreeMenu(sorted_menuList)
            # print(sysMenuList)
            serializerMenuList = list()
            for sysMenu in sysMenuList:
                serializerMenuList.append(SysMenuSerializer(sysMenu).data)
            roles = ','.join([role.name for role in roleList])
            # print(roles)
        except Exception as e:
            return JsonResponse({'code': 500, 'info': '账号或密码错误'})
        return JsonResponse({'code': 200, 'user': SysUserSerializer(user).data, 'token': token, 'info': 'OK',
                             "menuList": serializerMenuList, "role": roles})


class UserInfoUpdateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            # 校验id（转为整数，避免字符串id导致判断错误）
            user_id = int(data.get('id', -1))
            if user_id == -1:  # 新增
                pass
            else:  # 修改
                obj_sysUser = SysUser.objects.get(id=user_id)
                # 赋值字段
                obj_sysUser.phonenumber = data['phonenumber']
                obj_sysUser.email = data['email']

                # 保存并打印保存后的状态
                obj_sysUser.save()
                print("=== 第四步：执行save()完成 ===")

                # 保存后立即重新查询，验证是否写入数据库
                updated_user = SysUser.objects.get(id=user_id)
                print(f"重新查询验证：数据库中手机号={updated_user.phonenumber}，邮箱={updated_user.email}")

            return JsonResponse({'code': 200, 'info': 'OK'})
        except Exception as e:
            print(f"隐藏异常：{str(e)}")  # 兜底捕获所有可能的静默异常
            return JsonResponse({'code': 500, 'info': f'错误：{str(e)}'})


class PwdModifyView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            print(data)  # {"oldPassword":"123","newPassword":"123456","confirmPassword":"123456","id":1}
            obj_user = SysUser.objects.get(id=int(data['id']))
            print(obj_user)
            if obj_user.password == data['oldPassword']:
                if obj_user.password == data['newPassword']:
                    return JsonResponse({'code': 400, 'info': '新密码不能与旧密码相同'})
                obj_user.password = data['newPassword']
                obj_user.update_time = datetime.datetime.now().date()
                obj_user.save()
            else:
                return JsonResponse({'code': 400, 'info': '旧密码错误'})
        except Exception as e:
            return JsonResponse({'code': 400, 'info': f'错误：{str(e)}'})
        return JsonResponse({'code': 200, 'info': 'OK'})


class ImageView(View):
    def post(self, request):
        file = request.FILES.get('avatar')
        print("file:", file)
        if file:
            file_name = file.name
            suffixName = file_name[file_name.rfind("."):]
            new_file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + suffixName
            file_path = str(settings.MEDIA_ROOT) + "\\userAvatar\\" + new_file_name
            print("file_path:", file_path)
            try:
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                        return JsonResponse({'code': 200, 'title': new_file_name})
            except:
                return JsonResponse({'code': 500, 'errorInfo': '上传头像失败'})


class AvatarView(View):
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        print(data)
        id = data['id']
        avatar = data['avatar']
        obj_user = SysUser.objects.get(id=id)
        obj_user.avatar = avatar
        obj_user.save()
        return JsonResponse({'code': 200, 'newPickName': avatar})


class SearchView(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        pageNum = data['pageNum']
        pageSize = data['pageSize']
        print(pageSize, pageNum)
        UserList = Paginator(SysUser.objects.all(), pageSize).page(pageNum)
        obj_user = UserList.object_list.values()
        users = list(obj_user)
        total = SysUser.objects.count()
        return JsonResponse({'code': 200, 'userList': users, 'total': total})


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
