<template>
  <div class="nav-wrapper">
    <div
      class="tab-button"
      :class="{ active: route.path === tab.path }"
      v-for="(tab, index) in tabs"
      :key="index"
      @click="router.push(tab.path)"
    >
      <component class="icon" :is="tab.component" />
      <div class="label">{{ tab.label }}</div>
    </div>
  </div>
</template>

<script setup>
import { Cake, CakeSlice, CupSoda, House } from "@lucide/vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const router = useRouter();

const tabs = [
  { label: "首页", component: House, path: "/" },
  { label: "蛋糕", component: Cake, path: "/cake" },
  { label: "甜品", component: CakeSlice, path: "/dessert" },
  { label: "饮品", component: CupSoda, path: "/drink" },
];
</script>

<style lang="scss" scoped>
.nav-wrapper {
  display: flex;
  width: 7.5rem;
  max-width: 7.5rem;
  justify-content: space-around;
  position: fixed;
  padding: 0.2rem 0;
  bottom: 0;
  left: 0;
  color: #777;
  background-color: #d4dee5;
}

.tab-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.06rem;
  font-size: 0.22rem;
  cursor: pointer;
}

.icon {
  width: 0.36rem;
  height: 0.36rem;
}

.label {
  font-size: 0.2rem;
}

.active {
  color: #000 !important;
  font-weight: bold;
}
</style>
