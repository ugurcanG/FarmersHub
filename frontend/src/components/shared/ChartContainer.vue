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
          <LineChart :labels="labels" :data="lineData" :title="selectedLineData?.label || ''" />
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
          <BarChart :labels="labels" :data="barData" :title="selectedBarData?.label || ''" />
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import LineChart from 'src/components/shared/LineChart.vue'
import BarChart from 'src/components/shared/BarChart.vue'

const props = defineProps({
  title: { type: String, default: 'Messwerte-Analyse' },
  labels: { type: Array as () => string[], required: true }, // X-Achsen Labels
  data: { type: Array as () => any[], required: true }, // Alle Messwerte
  chartOptions: { type: Array as () => { label: string; value: string }[], required: true },
})

const selectedLineData = ref(props.chartOptions[0]) // Standard erste Option
const selectedBarData = ref(props.chartOptions[1]) // Standard zweite Option

const lineData = ref<number[]>([]);
const barData = ref<number[]>([]);

watch([selectedLineData, selectedBarData, props.data], () => {
  if (!props.data || props.data.length === 0) {
    lineData.value = [];
    barData.value = [];
    return;
  }

  lineData.value = props.data.map((m) => selectedLineData.value ? (m[selectedLineData.value.value] || 0) : 0);
  barData.value = props.data.map((m) => selectedBarData.value ? (m[selectedBarData.value.value] || 0) : 0);
});

</script>
