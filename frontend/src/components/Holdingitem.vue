<script setup lang="ts">
import type {Holding} from '../types/holding'
import {storeToRefs} from "pinia";
import {useAssetStore} from "../stores/assets";
import {computed, onMounted} from "vue";
import {useRouter} from "vue-router";

const props = defineProps<{
  holding: Holding,
  currentPrice: number
}>()

const currentPrice = computed(() => props.currentPrice)
const router = useRouter()

const assetStore = useAssetStore();
const {assets, loading} = storeToRefs(assetStore); // keeps reactivity when destructuring
onMounted(() => assetStore.load());

const asset = assetStore.byId.get(props.holding.assetId);

</script>

<template>

  <div class="flex flex-row gap-1 my-2 p-4 cursor-pointer whitespace-nowrap border-1 rounded-lg border-primary" @click="router.push('/stocks/' + asset?.ticker)">
    <p class="flex-1 min-w-0 truncate">{{ asset?.name }}</p>
    <p class="w-16 text-right">{{ props.holding.quantity }}</p>
    <p class="w-24 text-right">{{ currentPrice }}</p>
  </div>

</template>

<style scoped>

</style>