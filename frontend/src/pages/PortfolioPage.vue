<script setup lang="ts">
import StockChart from "../components/StockChart.vue";
import StockStats from "../components/StockStats.vue";
import {mockCandleChartData} from "../mocks/chart.ts";
import Holdingitem from "../components/Holdingitem.vue";
import {onMounted, ref} from "vue";
import {getHoldings} from "../scripts/holding.ts";
import {usePortfolioStore} from "../stores/portfolio.ts";
import type {Holding} from "../types/holding.ts";

const holdingRef = ref<Holding[]>([]);
const portfolioStore = usePortfolioStore();

onMounted(() => {
  getHoldings().then((holdings) => {
    holdingRef.value = holdings;
  })// no catch here because we want to handle the error in the getHoldings function itself
  portfolioStore.load()
})


</script>

<template>
  <div class="flex flex-col gap-2">
    <div class="flex flex-row gap-1 m-4">
      <StockChart :chartCandleData="mockCandleChartData" class="w-3/5"/>
      <div class="w-2/5">
        <StockStats :candleData="mockCandleChartData"/>
        <div>Cash Balance: {{ Number(portfolioStore.cashBalance).toFixed(2) }}</div>
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