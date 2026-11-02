<script setup lang="ts">
import StockChart from "../components/StockChart.vue";

defineProps<{
  symbol: string;
}>()
import {mockCandleChartData} from "../mocks/chart.ts";
import StockStats from "../components/StockStats.vue";

</script>

<template>
  <div class="flex flex-row gap-1 m-4">
    <StockChart :chartCandleData="mockCandleChartData" class="w-3/5"/>
    <StockStats :candle-data="mockCandleChartData" class="w-2/5"/>
  </div>
</template>

<style scoped>

</style>