<template>
  <canvas id="chartOne"></canvas>
</template>

<script>
import Chart from 'chart.js'

export default {
  name: "donutChart",
  props: {
    chartType: String,
    chartData: Object,
    chartOptions: Object
  },
  methods: {
    chartConstructor(chartType, chartData, chartOptions, canvasID) {
      console.log('chartConstructor fired', chartType)
      const chartElement = document.getElementById(canvasID)
      const chart = new Chart(chartElement, {
        type: chartType,
        data: chartData,
        options: chartOptions
      });
    },
  },
  mounted() {
    let {chartType,chartData,chartOptions} = this;
    this.chartConstructor(chartType, chartData, chartOptions, 'chartOne')
  }
}
</script>

<style scoped>

</style>
