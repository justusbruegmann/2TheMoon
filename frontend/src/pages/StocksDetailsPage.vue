<script setup lang="ts">
import {onMounted, ref} from 'vue'

import StockChart from "../components/StockChart.vue";
import StockStats from "../components/StockStats.vue";
import {mockCandleChartData} from "../mocks/chart.ts";
import {getPriceHistory} from "../scripts/price_history.ts";


const props = defineProps<{
  symbol: string;
}>()

const candleChartData = ref(mockCandleChartData);

onMounted(async () => {
  const data = await getPriceHistory(props.symbol);
  candleChartData.value = data;
});

</script>

<template>
  <div class="flex flex-row gap-1 m-4">
    <StockChart :chartCandleData="candleChartData" class="w-3/5"/>
    <StockStats :candle-data="candleChartData" class="w-2/5"/>
  </div>
</template>

<style scoped>

</style>