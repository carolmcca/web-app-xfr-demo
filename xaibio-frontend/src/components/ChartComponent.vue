<template> 
  <div class="chart">
    <canvas id="myChart"></canvas>
  </div>
</template>

<script>
  import Chart from 'chart.js/auto';

  export default {
    name: 'ChartComponent',
    props: ['data', 'color'],
    mounted() {
      const chart_data = {
        labels: Object.keys(this.data.responsibilities),
        datasets: [{
          label: 'Responsibilities',
          data: Object.values(this.data.responsibilities),
          borderColor: this.color,
          backgroundColor: this.color + "80",
          borderWidth: 2,
          borderRadius: Number.MAX_VALUE,
          borderSkipped: false,
        }]
      };
      const config = {
        type: 'bar',
        data: chart_data,
        options: { 
          scales: {
            x: [{ grid: { display: false } }],
            y: [{ grid: { display: false } }]
          },
          responsive: true,
          maintainAspectRatio: false, 
        }
      };
      const myChart = new Chart(
        document.getElementById('myChart'),
        config
      );
    }
  }
</script>

<style>
  canvas {
    height: 100%;
    width: 100%;
  }
  .chart {
    height: 100%;
    width: 100%;
    margin: auto;
  }
</style>