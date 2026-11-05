<script setup lang="ts">
import {onMounted, ref} from 'vue'

import StockChart from "../components/StockChart.vue";
import StockStats from "../components/StockStats.vue";
import {mockCandleChartData} from "../mocks/chart.ts";
import {getPriceHistory} from "../scripts/price_history.ts";
import {notify} from "../scripts/notify.ts";
import {calculateSummedUpCandleData} from "../utils/CalculateStockAnalyze.ts";

const props = defineProps<{
  symbol: string;
}>()

const candleChartData = ref(mockCandleChartData);
const thisMorning = new Date();
thisMorning.setHours(0, 0, 0, 0);
onMounted(async () => {
  const data = await getPriceHistory(props.symbol, thisMorning);
  candleChartData.value = data;
});

async function timeframeChanged(newTimeframe: string) {
  notify.info("Timeframe changed,", newTimeframe);
  if (newTimeframe === "1D") {
    candleChartData.value = await getPriceHistory(props.symbol, thisMorning);
  } else if (newTimeframe === "1W") {
    const oneWeekAgo = new Date();
      oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);
      oneWeekAgo.setHours(0, 0, 0, 0);
      const oneWeekData = await getPriceHistory(props.symbol, oneWeekAgo);
    candleChartData.value = calculateSummedUpCandleData(oneWeekData, "1W");
    }
  }

</script>

<template>
  <div class="flex flex-row gap-1 m-4">
    <StockChart :chartCandleData="candleChartData" class="w-3/5" @update:timeframe="timeframeChanged($event)"/>
    <StockStats :candle-data="candleChartData" class="w-2/5"/>
  </div>
</template>

<style scoped>

</style>