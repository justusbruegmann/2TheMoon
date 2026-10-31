<script setup lang="ts">
import StockChart from "../components/StockChart.vue";

defineProps<{
  symbol: string;
}>()
</script>

<template>
 <StockChart :symbol="symbol"  class="w-3/5"/>
</template>

<style scoped>

</style>