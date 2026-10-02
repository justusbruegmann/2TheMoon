<script setup lang="ts">
import {ref} from "vue";

const count = ref(0)

function countUp() {
  count.value++
}
</script>

<template>
  <button :value="count" @click="countUp" class="bg-gray-600 m-128 p-2">{{ count }}</button>
</template>
