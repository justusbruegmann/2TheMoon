<script setup lang="ts">
import StockChart from "../components/StockChart.vue";
import StockStats from "../components/StockStats.vue";
import {mockCandleChartData} from "../mocks/chart.ts";
import Holdingitem from "../components/Holdingitem.vue";
import {mockHoldings} from "../mocks/holding.ts";
import {ref} from "vue";

const holdingRef = ref(mockHoldings);
</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex flex-row gap-1 m-4">
      <StockChart :chartCandleData="mockCandleChartData" class="w-3/5"/>
      <div class="w-2/5">
        <StockStats :candleData="mockCandleChartData"/>
      </div>
    </div>
    <div class="px-4">
      Your Stocks:
      <div class="overflow-x-clip max-h-[45vh]  overflow-y-auto w-full">
        <Holdingitem v-for="holding in holdingRef" :key="holding.assetId" :holding="holding" :currentPrice="0"/>
      </div>

    </div>
  </div>
</template>

<style scoped>

</style>