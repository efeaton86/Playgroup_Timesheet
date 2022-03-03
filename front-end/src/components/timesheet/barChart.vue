<template>
  <canvas id="chartTwo"></canvas>
</template>

<script>
import Chart from 'chart.js'

export default {
  name: "barChart",
  props: {
    chartData: Object,
    chartOptions: Object,
    chartType: String
  },
  methods: {
    chartConstructor(chartType, chartData, chartOptions, canvasID) {
      const chartElement = document.getElementById(canvasID)
      const chart = new Chart(chartElement, {
        type: chartType,
        data: chartData,
        options: chartOptions
      });
    },
  },
  mounted() {
    let { chartData, chartOptions, chartType } = this;
    this.chartConstructor(chartType, chartData, chartOptions, 'chartTwo')
  },
}
</script>

<style scoped>

</style>
