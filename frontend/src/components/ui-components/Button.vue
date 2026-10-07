<script setup lang="ts">

import {computed, useAttrs} from "vue";

const props = withDefaults(defineProps<{
  variant?: "primary" | "success" | "info" | "warning" | "danger";
  label?: string;
  loading?: boolean;
}>(), {
  variant: "primary",
  label:"",
  loading:false,
})

const attrs = useAttrs()

const base = "inline-flex items-center justify-center font-medium focus:outline-none transition rounded-md p-2"
const variantClasses: Record<string,string> = {
  primary: 'bg-[var(--color-primary)] text-[var(--color-on-primary)] hover:bg-[var(--color-primary-hover)]',
  success: 'bg-green-500 text-white hover:bg-green-600',
  info: 'bg-blue-500 text-white hover:bg-blue-600',
  warning: 'bg-yellow-500 text-black hover:bg-yellow-600',
  danger: 'bg-red-600 text-white hover:bg-red-700',
}

const classes = computed(() => [
    base,
    variantClasses[props.variant]
].join(' '))

function handleClick(e: MouseEvent) {
  if (props.loading) {
    e.preventDefault()
    return
  }
}

</script>

<template>
<div>
  <button :class="[classes, attrs.class]" @click="handleClick">{{label}}</button>
</div>
</template>

<style scoped>

</style>