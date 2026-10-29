<script setup lang="ts">

import {computed} from "vue";

const props = defineProps<{
  title: string,
  width?: string,
}>()

const base = "h-auto bg-surface p-4 rounded-lg"

const style = computed(() => props.width ? {width: props.width} : undefined)
</script>

<template>
  <div :class="base" :style="style">
    <h1 class="text-text text-2xl font-bold">{{props.title}}</h1>
    <slot/>
    <slot name="footer"/>
  </div>

</template>

<style scoped>

</style>