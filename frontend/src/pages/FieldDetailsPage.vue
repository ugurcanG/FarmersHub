<template>
  <q-page class="q-pa-md">
    <!-- Basisdetails -->
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Details für Feld: {{ field.name }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Größe:</strong> {{ field.size }} ha</p>
        <p><strong>Saatgut:</strong> {{ field.saat__name || 'Kein Saatgut zugewiesen' }}</p>
        <p><strong>Erstellt am:</strong> {{ field.created_at }}</p>
        <p><strong>Health Score:</strong> {{ field.health_score }}</p>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>

    <!-- Tabelle der Messwerte -->
    <q-card class="q-pa-md shadow-2 q-mt-md">
      <q-card-section>
        <h4 class="text-h6">Messwerte</h4>
        <q-table
          :rows="measurements"
          :columns="columns"
          row-key="id"
          flat
          bordered
        >
          <template v-slot:top-right>
            <q-btn flat icon="refresh" @click="fetchMeasurements" label="Aktualisieren" />
          </template>
        </q-table>
      </q-card-section>
    </q-card>

    <!-- Diagramme -->
    <q-card class="q-pa-md shadow-2 q-mt-md">
      <q-card-section>
        <h4 class="text-h6">Messwerte-Analyse</h4>
        <q-separator class="q-mb-md" />
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <!-- Dropdown für Linendiagramm -->
            <q-select
              v-model="selectedLineData"
              :options="chartOptions"
              label="Linien-Daten auswählen"
              outlined
              dense
              class="q-mb-md"
            />
            <canvas id="lineChart"></canvas>
          </div>
          <div class="col-12 col-md-6">
            <!-- Dropdown für Balkendiagramm -->
            <q-select
              v-model="selectedBarData"
              :options="chartOptions"
              label="Balken-Daten auswählen"
              outlined
              dense
              class="q-mb-md"
            />
            <canvas id="barChart"></canvas>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from 'boot/axios';
import {
  Chart,
  LineController,
  BarController,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
} from 'chart.js';

// Registriere die notwendigen Chart.js-Komponenten
Chart.register(
  LineController,
  BarController,
  LineElement,
  BarElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip
);

const field = ref({
  id: 0,
  name: '',
  size: 0,
  created_at: '',
  saat__name: null,
  health_score: null,
});

interface Measurement {
  id: number;
  created_at: string;
  temperature: number;
  humidity: number;
  soil_moisture: number;
  nutrients_level: number;
  health_score: number;
}

const measurements = ref<Measurement[]>([]);
const columns = [
  { name: 'created_at', label: 'Datum', align: 'left' as const, field: 'created_at', sortable: true },
  { name: 'temperature', label: 'Temperatur (°C)', align: 'right' as const, field: 'temperature', sortable: true },
  { name: 'humidity', label: 'Luftfeuchtigkeit (%)', align: 'right' as const, field: 'humidity', sortable: true },
  { name: 'soil_moisture', label: 'Bodenfeuchte (%)', align: 'right' as const, field: 'soil_moisture', sortable: true },
  { name: 'nutrients_level', label: 'Nährstoffe', align: 'right' as const, field: 'nutrients_level', sortable: true },
  { name: 'health_score', label: 'Health Score', align: 'right' as const, field: 'health_score', sortable: true },
];

// Dropdown-Optionen für Diagramme
const chartOptions = [
  { label: 'Temperatur (°C)', value: 'temperature' },
  { label: 'Luftfeuchtigkeit (%)', value: 'humidity' },
  { label: 'Bodenfeuchte (%)', value: 'soil_moisture' },
  { label: 'Nährstoffe', value: 'nutrients_level' },
  { label: 'Health Score', value: 'health_score' },
];


// Standardauswahl
const selectedLineData = ref(chartOptions[0]); // Standard: Temperatur
const selectedBarData = ref(chartOptions[4]);  // Standard: Health Score


let lineChart: Chart | null = null;
let barChart: Chart | null = null;

const route = useRoute();
const router = useRouter();
const fieldId = String(route.params.id);

const fetchFieldDetails = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/`);
    field.value = response.data;
  } catch (error) {
    console.error('Fehler beim Abrufen der Felddetails:', error);
    await router.push('/fields');
  }
};

const fetchMeasurements = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/measurements/`);
    measurements.value = response.data;
    console.log('Fetched Measurements:', measurements.value); // Log die rohen Messwerte
    renderCharts(); // Initialisiere die Diagramme
  } catch (error) {
    console.error('Fehler beim Abrufen der Messwerte:', error);
  }
};

const renderCharts = () => {
  const lineCanvas = document.getElementById('lineChart') as HTMLCanvasElement | null;
  const barCanvas = document.getElementById('barChart') as HTMLCanvasElement | null;

  const labels = measurements.value.map(m => new Date(m.created_at).toLocaleDateString());

  const lineData = measurements.value.map(m => {
    const key = selectedLineData.value?.value as keyof Measurement;
    if (!Object.keys(m).includes(key)) {
      console.error(`Invalid key "${key}" for line chart`);
      return 0;
    }
    return m[key] as number || 0;
  });

  const barData = measurements.value.map(m => {
    const key = selectedBarData.value?.value as keyof Measurement;
    if (!Object.keys(m).includes(key)) {
      console.error(`Invalid key "${key}" for bar chart`);
      return 0;
    }
    return m[key] as number || 0;
  });

  console.log('Chart Labels:', labels);
  console.log('Line Chart Data:', lineData);
  console.log('Bar Chart Data:', barData);

  if (lineCanvas) {
    if (lineChart) lineChart.destroy();
    lineChart = new Chart(lineCanvas.getContext('2d')!, {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: chartOptions.find(o => o.value === selectedLineData.value?.value)?.label || '',
            data: lineData,
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2,
            fill: false,
          },
        ],
      },
    });
  }

  if (barCanvas) {
    if (barChart) barChart.destroy();
    barChart = new Chart(barCanvas.getContext('2d')!, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: chartOptions.find(o => o.value === selectedBarData.value?.value)?.label || '',
            data: barData,
            backgroundColor: 'rgba(153, 102, 255, 0.6)',
            borderWidth: 1,
          },
        ],
      },
    });
  }
};

// Watcher aktualisiert Diagramme bei Auswahländerung
watch([selectedLineData, selectedBarData], () => {
  console.log('Selected Line Data:', selectedLineData.value); // Debugging
  console.log('Selected Bar Data:', selectedBarData.value); // Debugging
  renderCharts();
});

// Cleanup bei Entladen der Komponente
onBeforeUnmount(() => {
  if (lineChart) lineChart.destroy();
  if (barChart) barChart.destroy();
});

const goBack = async () => {
  await router.push('/fields');
};

// Initialisierung
onMounted(async () => {
  await fetchFieldDetails();
  await fetchMeasurements();
});
</script>
