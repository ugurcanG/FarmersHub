<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { Chart, BarController, BarElement, LinearScale, CategoryScale, Tooltip, Title } from 'chart.js'

// Chart.js Komponenten registrieren
Chart.register(BarController, BarElement, LinearScale, CategoryScale, Tooltip, Title)

const props = defineProps({
  labels: { type: Array as () => string[], required: true }, // X-Achsen-Beschriftungen
  data: { type: Array as () => number[], required: true }, // Y-Achsen-Werte
  title: { type: String, default: 'Balkendiagramm' }, // Titel des Diagramms
})

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

// Funktion zum Erstellen des Balkendiagramms
const renderChart = () => {
  if (chartInstance) chartInstance.destroy() // Altes Diagramm zerstören
  if (!chartCanvas.value) return

  chartInstance = new Chart(chartCanvas.value.getContext('2d')!, {
    type: 'bar',
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.title,
          data: props.data,
          backgroundColor: 'rgba(54, 162, 235, 0.6)', // Blau
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  })
}

// Beim Laden & bei Änderungen der Daten Diagramm aktualisieren
onMounted(renderChart)
watch(() => [props.labels, props.data], renderChart)

onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy();
});

</script>
