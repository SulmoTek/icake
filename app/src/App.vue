<script setup>

import Tabbar from '@/components/Tabbar.vue';
import { useTabbar } from '@/stores/layout';

const tabbar = useTabbar();
</script>

<template>
  <div class="app-wrapper">
    <button @click="tabbar.toggle()">切换</button>
    <div class="main">
      <RouterView></RouterView>
    </div>
    <Tabbar v-if="tabbar.visiable"></Tabbar>
  </div>
</template>

<style scoped>
.app-wrapper {
  height: 100vh;
  max-height: 100vh;
}
</style>
