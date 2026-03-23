from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework_jwt.settings import api_settings

from menu.models import SysMenu, SysMenuSerializer
from role.models import SysRole
from user.models import SysUser, SysUserSerializer


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
                             "menuList": serializerMenuList,"role":roles})


class UserInfoUpdateView(View):
    def post(self, request):
        try:
            username = request.POST.get('username')
            phonenumber = request.POST.get('phonenumber')
            email = request.POST.get('email')
            
            # 获取当前用户（从token中解析）
            token = request.META.get('HTTP_AUTHORIZATION')
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            payload = jwt_decode_handler(token)
            user_id = payload.get('user_id')
            
            # 更新用户信息
            user = SysUser.objects.get(id=user_id)
            if phonenumber:
                user.phonenumber = phonenumber
            if email:
                user.email = email
            user.save()
            
            return JsonResponse({'code': 200, 'info': '更新成功'})
        except Exception as e:
            return JsonResponse({'code': 500, 'info': str(e)})



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