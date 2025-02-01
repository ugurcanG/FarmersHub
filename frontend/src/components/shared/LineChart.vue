<template>
  <canvas ref="chartCanvas"></canvas>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { Chart, LineController, LineElement, LinearScale, PointElement, CategoryScale, Tooltip, Title } from 'chart.js'

// Chart.js Komponenten registrieren
Chart.register(LineController, LineElement, LinearScale, PointElement, CategoryScale, Tooltip, Title)

// Props mit TypeScript-Typisierung
const props = defineProps({
  labels: { type: Array as () => string[], required: true }, // X-Achsen-Beschriftungen
  data: { type: Array as () => number[], required: true }, // Y-Achsen-Werte
  title: { type: String, default: 'Liniendiagramm' }, // Diagrammtitel
  lineColor: { type: String, default: 'rgba(75, 192, 192, 1)' }, // Standardfarbe (Türkis)
  fill: { type: Boolean, default: false }, // Soll die Linie gefüllt sein?
})

const chartCanvas = ref<HTMLCanvasElement | null>(null)
let chartInstance: Chart | null = null

// Funktion zum Erstellen des Liniendiagramms
const renderChart = () => {
  if (chartInstance) chartInstance.destroy() // Altes Diagramm zerstören
  if (!chartCanvas.value) return

  chartInstance = new Chart(chartCanvas.value.getContext('2d')!, {
    type: 'line',
    data: {
      labels: props.labels,
      datasets: [
        {
          label: props.title,
          data: props.data,
          borderColor: props.lineColor,
          borderWidth: 2,
          fill: props.fill,
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

// Aktualisieren bei Änderungen der Props
onMounted(renderChart)
watch(() => [props.labels, props.data], renderChart)

// Zerstören der Chart-Instanz, wenn die Komponente entfernt wird
onBeforeUnmount(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>
