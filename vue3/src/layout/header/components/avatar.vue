<template>
  <el-avatar shape="square" :size="40" :src="squareUrl"/>

  <el-dropdown>
    <span class="el-dropdown-link">
      &nbsp;&nbsp; {{ currentUser.username }}
      <el-icon class="el-icon--right">
        <arrow-down/>
      </el-icon>
    </span>
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item>
          <router-link :to="{name:'个人中心'}">个人中心</router-link>
        </el-dropdown-item>
        <el-dropdown-item @click="logOut">安全退出</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup>
import {ArrowDown} from '@element-plus/icons-vue'
import requestUtil from '@/util/request'
import router from "@/router";
import store from '@/store'

const currentUser = JSON.parse(sessionStorage.getItem("currentUser"));
const squareUrl = requestUtil.getServerUrl() + '/media/userAvatar/' + currentUser.avatar

const logOut = () => {
  sessionStorage.clear()
  store.commit('RESET_TAB')
  router.replace('/login')
}
</script>

<style scoped>
.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}

.el-tabs--card > .el-tabs__header .el-tabs__item.is-active {
  background-color: lightgray;
}

.el-main {
  padding: 0px;
}
</style>