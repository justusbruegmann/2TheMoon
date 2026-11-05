<script setup lang="ts">
import type {CandleChartData} from "../types/chart.ts";
import * as stats from "../utils/CalculateStockAnalyze.ts";
import {computed} from "vue";

const props = defineProps<{
  candleData: CandleChartData[]
}>()

const performance = computed(() => {
  if (props.candleData.length < 2) return 0;
  const first = props.candleData[0].close;
  const last = props.candleData[props.candleData.length - 1].close;
  return ((last - first) / first) * 100;
})

</script>

<template>
  <div class="stock-stats">
    <p :class="performance >=0 ? 'text-buy' : 'text-sell'">Performance: {{ performance.toFixed(2) }}%</p>
    <p>Minimum: {{ stats.calculateStockAnalyze(props.candleData).min }}</p>
    <p>Maximum: {{ stats.calculateStockAnalyze(props.candleData).max }}</p>
    <p>Open: {{ props.candleData[0]?.open ?? '-' }}</p>
    <p>Close: {{ props.candleData[props.candleData.length - 1]?.close ?? '-' }}</p>
  </div>
</template>

<style scoped>

</style>