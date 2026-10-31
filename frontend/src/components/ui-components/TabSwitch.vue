<script setup lang="ts">
import {type PropType} from 'vue'
import {Capitalize} from "../../utils/StringUtils.ts";

const props = defineProps({
  options: {type: Array as PropType<string[]>, required: true},
  fullWidth: { type: Boolean, default: false },
})

// the clicked tab, synced with the parent's v-model
const selected = defineModel<string>()

</script>

<template>
<div :class="['flex flex-row items-center gap-8', props.fullWidth ? 'w-full justify-center' : '']">
  <div v-for="item in props.options" :key="item" class="flex flex-col items-center">
    <button
        :class="['px-4 py-2 rounded-t-lg', selected === item ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700']"
        @click="selected = item"
    >
      {{ Capitalize(item) }}
    </button>
  </div>

</div>
</template>

<style scoped>

</style>