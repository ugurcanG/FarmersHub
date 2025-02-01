<!-- src/components/shared/EntityCharts.vue -->
<template>
  <ChartContainer
    :title="chartTitle"
    :labels="labels"
    :lineData="lineData"
    :barData="barData"
    :chartOptions="chartOptions"
    :selectedLineData="selectedLineData"
    :selectedBarData="selectedBarData"
  />
</template>

<script setup lang="ts">
import ChartContainer from 'src/components/shared/ChartContainer.vue'

defineProps({
  chartTitle: { type: String, required: true }, // z. B. "Feld-Analyse" oder "Maschinen-Analyse"
  labels: Array,
  lineData: Array,
  barData: Array,
  chartOptions: Array,
  selectedLineData: Object,
  selectedBarData: Object,
})
</script>
