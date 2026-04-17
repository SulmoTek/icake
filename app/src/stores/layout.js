import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTabbar = defineStore('tabbar', () => {
    const visiable = ref(true)

    const show = () => visiable.value = true;
    const hide = () => visiable.value = false;
    const toggle = () => visiable.value = !visiable.value;

    return {visiable, show, hide, toggle}
})
