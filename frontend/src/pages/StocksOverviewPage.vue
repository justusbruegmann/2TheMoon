<script setup lang="ts">

import {computed, onMounted, ref} from 'vue'
import {mockAssets} from "../mocks/assets.ts";
import {type Asset} from "../types/asset.ts";
import AssetItem from "../components/AssetItem.vue";

const data = ref<Asset[]>([]);
const searchValue = ref("");

const filteredData = computed(() => {
  const query = searchValue.value.trim().toLowerCase();
  return data.value.filter(entry =>
      entry.name.toLowerCase().includes(query) || entry.ticker.toLowerCase().includes(query)
  );
});


onMounted(() => {
  data.value = mockAssets;
})

</script>

<template>
  <div class="overflow-x-clip">
  <br>
  <div class="flex flex-row-reverse px-8 ">
    <input type="search" placeholder="Search..." class="border border-text-muted rounded-md pl-1"
           v-model="searchValue"/>
  </div>
  <div class="max-h-[85vh]  overflow-y-auto">
    <div v-for="asset in filteredData" :key="asset.id" class="px-8 py-4 ">
      <AssetItem :asset="asset"/>
    </div>
  </div>
  </div>

</template>

<style scoped>

</style>