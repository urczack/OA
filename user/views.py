from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework_jwt.settings import api_settings

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
        username = request.GET.get('username')
        password = request.GET.get('password')
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
            print("=== 第一步：接收的原始数据 ===")
            print(f"数据内容：{data}")
            print(f"data['id'] 的值：{data.get('id')}")
            print(f"data['id'] 的类型：{type(data.get('id'))}")  # 重点看类型（字符串/数字）

            # 校验id（转为整数，避免字符串id导致判断错误）
            user_id = int(data.get('id', -1))
            print(f"=== 第二步：转换后的用户ID ===")
            print(f"转换后id：{user_id}，是否等于-1：{user_id == -1}")

            if user_id == -1:  # 新增
                print("=== 第三步：走【新增】分支，未执行修改逻辑 ===")
                pass
            else:  # 修改
                print("=== 第三步：走【修改】分支 ===")
                obj_sysUser = SysUser.objects.get(id=user_id)
                print(f"找到用户：ID={obj_sysUser.id}，原手机号={obj_sysUser.phonenumber}，原邮箱={obj_sysUser.email}")

                # 赋值字段
                obj_sysUser.phonenumber = data['phonenumber']
                obj_sysUser.email = data['email']
                print(f"赋值后：新手机号={obj_sysUser.phonenumber}，新邮箱={obj_sysUser.email}")

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
