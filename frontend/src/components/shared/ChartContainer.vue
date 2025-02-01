<template>
  <q-card class="q-pa-md shadow-2">
    <q-card-section>
      <h4 class="text-h6">{{ title }}</h4>
      <q-separator class="q-mb-md" />
      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-6">
          <q-select
            v-model="selectedLineData"
            :options="chartOptions"
            label="Linien-Daten auswählen"
            outlined
            dense
            class="q-mb-md"
          />
          <div class="chart-container">
            <LineChart :labels="labels" :data="lineData" :title="selectedLineData?.label || ''" />
          </div>
        </div>
        <div class="col-12 col-md-6">
          <q-select
            v-model="selectedBarData"
            :options="chartOptions"
            label="Balken-Daten auswählen"
            outlined
            dense
            class="q-mb-md"
          />
          <div class="chart-container">
            <BarChart :labels="labels" :data="barData" :title="selectedBarData?.label || ''" />
          </div>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, watchEffect, onMounted } from 'vue';
import LineChart from 'src/components/shared/LineChart.vue';
import BarChart from 'src/components/shared/BarChart.vue';

const props = defineProps({
  title: { type: String, default: 'Messwerte-Analyse' },
  labels: { type: Array as () => string[], required: true },
  data: { type: Array as () => Array<{ [key: string]: number }>, required: true },
  chartOptions: { type: Array as () => { label: string; value: string }[], required: true },
});

const selectedLineData = ref(props.chartOptions[0] || null); // Erste Option als Standard setzen
const selectedBarData = ref(props.chartOptions[1] || null); // Zweite Option als Standard setzen

const lineData = ref<number[]>([]);
const barData = ref<number[]>([]);

// Daten aktualisieren, wenn sich etwas ändert
const updateChartData = () => {
  if (!props.data || props.data.length === 0) {
    lineData.value = [];
    barData.value = [];
    return;
  }

  lineData.value = props.data.map((m) =>
    selectedLineData.value ? m[selectedLineData.value.value] || 0 : 0
  );
  barData.value = props.data.map((m) =>
    selectedBarData.value ? m[selectedBarData.value.value] || 0 : 0
  );
};

watchEffect(() => {
  if (!props.data || props.data.length === 0 || !selectedLineData.value || !selectedBarData.value) {
    lineData.value = [];
    barData.value = [];
    return;
  }

  lineData.value = props.data.map((m) =>
    selectedLineData.value ? m[selectedLineData.value.value] || 0 : 0
  );
  barData.value = props.data.map((m) =>
    selectedBarData.value ? m[selectedBarData.value.value] || 0 : 0
  );
});
onMounted(updateChartData); // Direkt ausführen, damit Werte beim Laden da sind
</script>

<style scoped>
.chart-container {
  height: 300px; /* Feste Höhe für das Chart */
  max-height: 400px;
  min-height: 250px;
  width: 100%;
  position: relative;
}
</style>
