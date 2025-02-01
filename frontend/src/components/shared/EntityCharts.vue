<template>
  <div class="chart-wrapper">
    <ChartContainer
      :title="title"
      :labels="labels"
      :data="formattedData"
      :chartOptions="chartOptions"
    />
  </div>
</template>

<script setup lang="ts">
import ChartContainer from 'src/components/shared/ChartContainer.vue'

defineProps<{
  title: string
  labels: string[]
  formattedData: { [key: string]: number }[]
  chartOptions: { label: string; value: string }[]
}>()
</script>

<style scoped>
.chart-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: auto;
}
</style>
