<script setup lang="ts">
import Button from "./ui-components/Button.vue";

defineProps<{
  label: string;
}>()

function handleClick() {
  alert("hi");
}

</script>

<template>
<div class="bg-surface w-screen h-16 absolute">
  <div class="flex flex-row w-full">
    <img src="../assets/logo.png" alt="2TheMoon Logo" class="w-12 m-2" />
    <div class="text-text mt-4.5">{{label}}</div>
    <Button  label="login" @click="handleClick"/>
  </div>

</div>
</template>

<style scoped>

</style>