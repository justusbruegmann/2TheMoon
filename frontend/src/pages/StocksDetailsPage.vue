<script setup lang="ts">
import StockChart from "../components/StockChart.vue";

defineProps<{
  symbol: string;
}>()
</script>

<template>
  <div class="flex flex-row gap-1 m-4">
    <StockChart :symbol="symbol" class="w-3/5"/>
    <div class="w-2/5">Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et
      dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita
      kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur
      sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam
      voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata
      sanctus est Lorem ipsum dolor sit amet.
    </div>
  </div>
</template>

<style scoped>

</style>