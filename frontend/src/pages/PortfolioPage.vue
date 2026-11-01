<script setup lang="ts">
import StockChart from "../components/StockChart.vue";
import StockStats from "../components/StockStats.vue";
import {mockCandleChartData} from "../mocks/chart.ts";
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex flex-row gap-1 m-4">
      <StockChart :chartCandleData="mockCandleChartData" class="w-3/5"/>
      <div class="w-2/5">
        <StockStats :candleData="mockCandleChartData"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>