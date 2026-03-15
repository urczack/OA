<template>

  <el-button type="primary" @click="handlerLogin"> 测试登录</el-button>
  <el-button type="success" @click="handlerUserList">测试获取用户信息列表</el-button>
</template>

<script setup>
import requestUtil from "@/util/request"

const handlerLogin = async () => {
  let result = await requestUtil.get('user/jwt_test')
  let data = result.data;
  if (data.code == 200) {
    const token = data.token;
    console.log('登陆成功！token = ' + token)
    window.sessionStorage.setItem("token", token)
  } else {
    console.log('登陆失败！')
  }
}

const handlerUserList = async () => {
  let result = await requestUtil.get('user/test')
  let data = result.data;
  if (data.code == 200) {
    const UserList = data.data;
    console.log('用户信息列表 userList : ' + UserList)

  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
