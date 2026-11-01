<script setup lang="ts">
import {ref} from "vue";
import type {ApexOptions} from "apexcharts";
import TabSwitch from "./ui-components/TabSwitch.vue";
import type {CandleChartData, LineChartData} from "../types/chart.ts";

const props = defineProps<{
  chartCandleData: CandleChartData[];
}>()

const isCandleChart = ref<string>("Candle Chart")
const timeframe = ref<string>("1D")

// ApexCharts candles as { x: timestamp, y: [open, high, low, close] }
const seriesCandle = ref([{
  name: "Stock Price",
  data: props.chartCandleData.map(c => ({x: c.timestamp, y: [c.open, c.high, c.low, c.close]})),
}])

const seriesLine = ref([{
  name: "Stock Price",
  data: getMockLineChartData().map(c => ({x: c.timestamp, y: c.value})),
}])

 function getMockLineChartData(): LineChartData[] {
  return props.chartCandleData.map(c => ({
    timestamp: c.timestamp,
    value: +((c.open + c.high + c.low + c.close) / 4).toFixed(2),
  }))
}

const optionsCandle = ref<ApexOptions>({
  chart: {
    type: "candlestick",
    background: "#111A38",
    foreColor: "#8C96B8",
    fontFamily: "inherit",
    toolbar: {
      show: true,
      offsetX: -50,
      tools: {
        selection: true,
        reset: true,
        zoom: true,
        pan: true,
        measure: true,
        download: false,
        zoomin: false,
        zoomout: false,
      }
    },
    zoom: {enabled: true},
    animations: {enabled: true},
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
    events: {
      zoomed: (chartContext, options) => recolor(chartContext, options?.xaxis.min, options?.xaxis.max),
      scrolled: (chartContext, options) => recolor(chartContext, options?.xaxis.min, options?.xaxis.max),
    },
    background: "#111A38",
    foreColor: "#38BDF8",
    fontFamily: "inherit",
    toolbar: {
      show: true,
      offsetX: -50,
      tools: {
        selection: true,
        reset: true,
        zoom: true,
        pan: true,
        measure: true,
        download: false,
        zoomin: false,
        zoomout: false,
      }
    },
    zoom: {enabled: true},
    animations: {enabled: true},
  },
  colors: [getLineColor(undefined, undefined)],  theme: {mode: "dark"},
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

function recolor(chartContext: any, min?: number, max?: number) {
  setTimeout(() => {
    chartContext.updateOptions(
        {colors: [getLineColor(min, max)]},
        false, // redrawPaths
        false, // animate
        true,  // updateSyncedCharts
        false  // overwriteInitialConfig ← keeps reset working
    )
  })
}

function getLineColor(min: number | undefined, max: number | undefined): string {

  const visible = getMockLineChartData().filter(p =>
      (min === undefined || p.timestamp >= min) &&
      (max === undefined || p.timestamp <= max)
  )
  if (visible.length < 2) return "#38BDF8"
  const firstValue = visible[0].value
  const lastValue = visible[visible.length - 1].value
  if (lastValue > firstValue) return "#2BD97F"
  if (lastValue < firstValue) return "#F04A5C"
  return "#38BDF8"
}

const tabSwitchOptions = ref(["Candle Chart", "Line Chart"])
const tabTimeOptions = ref(["1D", "1W", "1M", "3M"])

</script>

<template>
  <div class="stock-chart">
    <div class="flex flex-row justify-between items-center mb-4">
      <TabSwitch v-model="isCandleChart" :options="tabSwitchOptions"/>
      <TabSwitch v-model="timeframe" :options="tabTimeOptions"/>
    </div>

    <apexchart v-if="isCandleChart === 'Candle Chart'" width="100%" height="350" type="candlestick"
               :options="optionsCandle" :series="seriesCandle"></apexchart>
    <apexchart v-else width="100%" height="350" type="line" :options="optionsLine" :series="seriesLine"></apexchart>
  </div>
</template>

<style scoped>

</style>
