<script setup lang="ts">
import {ref} from 'vue'

const series = ref([{name: "HomeChart", data: [17, 20, 27, 27, 25,28,33, 35], color: "#2BD97F"}])
const options = ref({
  chart: {
    type: "area",
    toolbar: {
      show: false
    },
    zoom: {enabled: false},
    sparkline: {enabled: true},
  },
  series: series.value,
  stroke: {
    width: 3,
    curve: "straight",
  },
  xaxis: {
    categories: series.value
  },
  fill: {
    type: "solid",
    opacity: 0.25
  },
  colors: ["#2BD97F"],
  tooltip: {
    enabled: false
  },
})

</script>

<template>
  <div class="flex flex-row justify-center items-center w-full gap-8">
    <div>
      <h1 class="text-2xl font-bold mt-25">2TheMoon Stock Simulator</h1>
      <p>Trade stock and crypto with virtual money and other players </p>
      <p>Sign up and get 10.000€ start money</p>
    </div>

    <div class=" mt-15">
      <div class="bg-line p-4 rounded-lg relative ">
        <h3 class="absolute top-4 left-4 z-10 text-white font-bold">Portfolio</h3>
        <div class="absolute top-12 left-4 z-10">
          <p class="bg-buy text-black px-2 py-1 rounded font-bold">+24.5%</p>
        </div>
        <apexchart width="400" type="area" :options="options" :series="series"></apexchart>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>