<script setup lang="ts">
import {useRouter} from 'vue-router'
import type {Asset} from "../types/asset.ts";

const props = defineProps<{ asset: Asset }>();
const router = useRouter()

</script>

<template>
<div class="border border-text-muted rounded-lg grid grid-cols-[2fr_2fr_1fr_1fr] gap-4 p-4" @click="router.push('/stocks/'+ props.asset.ticker)">
  <p>{{props.asset.name}}</p>
  <p>{{props.asset.industry.join(', ')}}</p>
  <p class="text-right">1074.5€</p>
  <p class="text-right">+24.24%</p>
</div>
</template>

<style scoped>

</style>