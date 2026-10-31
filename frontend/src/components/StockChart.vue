<script setup lang="ts">
import {ref} from "vue";
import type {ApexOptions} from "apexcharts";
import {mockCandleChartData, mockLineChartData} from "../mocks/chart.ts";
import TabSwitch from "./ui-components/TabSwitch.vue";

const isCandleChart = ref<string>("Candle Chart")

// ApexCharts expects candles as { x: timestamp, y: [open, high, low, close] }
const seriesCandle = ref([{
  name: "Stock Price",
  data: mockCandleChartData.map(c => ({x: c.timestamp, y: [c.open, c.high, c.low, c.close]})),
}])

const seriesLine = ref([{
  name: "Stock Price",
  data: mockLineChartData.map(c => ({x: c.timestamp, y: c.value})),
  color: getLineColor(),
}])

const optionsCandle = ref<ApexOptions>({
  chart: {
    type: "candlestick",
    background: "transparent",
    foreColor: "#8C96B8",
    fontFamily: "inherit",
    toolbar: {show: false},
    zoom: {enabled: false},
    animations: {enabled: false},
  },
  theme: {mode: "dark"},
  plotOptions: {
    candlestick: {
      colors: {
        upward: "#2BD97F",
        downward: "#F04A5C",
      },
      wick: {useFillColor: true},
    },
  },
  xaxis: {
    type: "datetime",
    labels: {datetimeUTC: false},
    axisBorder: {color: "#28335A"},
    axisTicks: {color: "#28335A"},
    tooltip: {enabled: false},
  },
  yaxis: {
    opposite: true,
    tooltip: {enabled: true},
    labels: {formatter: (value: number) => value.toFixed(2)},
  },
  grid: {
    borderColor: "#28335A",
    strokeDashArray: 4,
  },
  tooltip: {
    theme: "dark",
    x: {format: "dd MMM HH:mm"},
  },
})

const optionsLine = ref<ApexOptions>({
  chart: {
    type: "line",
    background: "transparent",
    foreColor: "#38BDF8",
    fontFamily: "inherit",
    toolbar: {show: false},
    zoom: {enabled: false},
    animations: {enabled: false},
  },
  theme: {mode: "dark"},
  colors: ["#38BDF8"],
  stroke: {
    width: 2,
    curve: "straight",
  },
  markers: {
    size: 0,
    hover: {size: 4},
  },
  xaxis: {
    type: "datetime",
    labels: {datetimeUTC: false},
    axisBorder: {color: "#28335A"},
    axisTicks: {color: "#28335A"},
    tooltip: {enabled: false},
  },
  yaxis: {
    opposite: true,
    labels: {formatter: (value: number) => value.toFixed(2)},
  },
  grid: {
    borderColor: "#28335A",
    strokeDashArray: 4,
  },
  tooltip: {
    theme: "dark",
    x: {format: "dd MMM HH:mm"},
    y: {formatter: (value: number) => value.toFixed(2)},
  },
})

function getLineColor(): string {
  const firstValue = mockLineChartData[0].value
  const value = mockLineChartData[mockLineChartData.length - 1].value
  if (value > firstValue) return "#2BD97F"
  if (value < firstValue) return "#F04A5C"
  return "#38BDF8"
}

const tabSwitchOptions = ref(["Candle Chart", "Line Chart"])

</script>

<template>
  <div class="stock-chart">
    <div class="flex flex-row justify-between items-center mb-4">
      <TabSwitch v-model="isCandleChart" :options="tabSwitchOptions" />
      <!-- right side: second control goes here -->
    </div>
    <apexchart v-if="isCandleChart === 'Candle Chart'" width="100%" height="350" type="candlestick" :options="optionsCandle" :series="seriesCandle"></apexchart>
    <apexchart v-else width="100%" height="350" type="line" :options="optionsLine" :series="seriesLine"></apexchart>
  </div>
</template>

<style scoped>

</style>
