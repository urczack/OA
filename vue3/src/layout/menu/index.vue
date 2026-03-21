<template>
  <el-menu
      ctive-text-color="#ffd04b"
      background-color="#2d3a4b"
      class="el-menu-vertical-demo"
      text-color="#fff"
      :default-active="'/index'"
      router
      @open="handleOpen"
      @close="handleClose"
  >
    <el-menu-item index="/index" @click="openTab({name:'首页',path:'/index'})">
      <el-icon>
        <home-filled/>
      </el-icon>
      <span>首页</span>
    </el-menu-item>

    <el-sub-menu :index="menu.path" v-for="menu in menuList">
      <template #title>
        <el-icon>
          <svg-icon :icon="menu.icon"></svg-icon>
        </el-icon>
        <span>{{ menu.name }}</span>
      </template>
      <el-menu-item :index="item.path" v-for="item in menu.children" @click="openTab(item)">
        <el-icon>
          <svg-icon :icon="item.icon"></svg-icon>
        </el-icon>
        <span>{{ item.name }}</span>
      </el-menu-item>


    </el-sub-menu>
  </el-menu>
</template>

<script setup>
import {
  HomeFilled
} from '@element-plus/icons-vue'
import store from '@/store'


const menuList = JSON.parse(sessionStorage.getItem("menuList"))

const openTab = (item) => {
  store.commit('ADD_TABS', item)
}
</script>


<style lang="scss" scoped>


</style>