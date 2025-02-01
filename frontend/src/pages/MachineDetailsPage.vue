<template>
  <q-page class="q-pa-md">
    <!-- Basisdetails -->
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Maschinendetails: {{ machine.name || 'Lädt...' }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Status:</strong> {{ machine.status || 'Unbekannt' }}</p>
        <p><strong>Kategorie:</strong> {{ machine.category || 'Unbekannt' }}</p>
        <p><strong>Seriennummer:</strong> {{ machine.serial_number || 'Keine Seriennummer' }}</p>
        <p><strong>Baujahr:</strong> {{ machine.year_of_manufacture ?? 'Unbekannt' }}</p>
        <p><strong>Betriebsstunden:</strong> {{ machine.operating_hours ?? 0 }} h</p>
        <p><strong>Zugewiesenes Feld:</strong> {{ machine.assigned_field?.name ?? 'Kein Feld zugewiesen' }}</p>
        <p><strong>Mitarbeiter:</strong>
          <span v-if="machine.assigned_employees && machine.assigned_employees.length > 0">
            {{ machine.assigned_employees.map(e => `${e.first_name} ${e.last_name}`).join(', ') }}
          </span>
          <span v-else>Keine Mitarbeiter zugewiesen</span>
        </p>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>

    <!-- Tabelle der Maschinenmesswerte -->
    <q-card class="q-pa-md shadow-2 q-mt-md">
      <q-card-section>
        <h4 class="text-h6">Messwerte</h4>
        <q-table :rows="measurements" :columns="columns" row-key="id" flat bordered>
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
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'
import type { Machine, MachineMeasurement } from 'src/components/models';
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
} from 'chart.js'

// Registriere Chart.js-Komponenten
Chart.register(LineController, BarController, LineElement, BarElement, PointElement, LinearScale, CategoryScale, Title, Tooltip)

// Routen-Setup
const route = useRoute()
const router = useRouter()
const machineId = String(route.params.id)

// Maschinen-Daten
const machine = ref<Machine>({
  id: 0,
  name: '',
  status: '',
  category: '',
  serial_number: "",
  year_of_manufacture: 0,
  operating_hours: 0,
  assigned_field: null,
  assigned_employees: []
})

// Maschinenmesswerte
const measurements = ref<MachineMeasurement[]>([])
const columns = [
  { name: 'recorded_at', label: 'Datum', align: 'left' as const, field: 'recorded_at', sortable: true },
  { name: 'fuel_level', label: 'Benzinstand (%)', align: 'right' as const, field: 'fuel_level', sortable: true },
  { name: 'engine_temperature', label: 'Motortemperatur (°C)', align: 'right' as const, field: 'engine_temperature', sortable: true },
  { name: 'oil_level', label: 'Ölstand (%)', align: 'right' as const, field: 'oil_level', sortable: true },
  { name: 'rpm', label: 'RPM', align: 'right' as const, field: 'rpm', sortable: true },
]

// Dropdown-Optionen für Diagramme
const chartOptions = [
  { label: 'Benzinstand (%)', value: 'fuel_level' },
  { label: 'Motortemperatur (°C)', value: 'engine_temperature' },
  { label: 'Ölstand (%)', value: 'oil_level' },
  { label: 'RPM', value: 'rpm' },
]

const selectedLineData = ref(chartOptions[0]) // Standard: Benzinstand
const selectedBarData = ref(chartOptions[1])  // Standard: Motortemperatur

let lineChart: Chart | null = null
let barChart: Chart | null = null

// Zurück-Navigation
const goBack = () => {
  router.back()
}

// API: Maschineninfos abrufen
const fetchMachineDetails = async () => {
  try {
    const response = await api.get(`/machines/${machineId}/`)
    machine.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinendetails:', error)
    await router.push('/machines')
  }
}

// API: Maschinenmesswerte abrufen
const fetchMeasurements = async () => {
  try {
    const response = await api.get(`/machines/${machineId}/measurements/`)
    measurements.value = response.data
    renderCharts()
  } catch (error) {
    console.error('Fehler beim Abrufen der Messwerte:', error)
  }
}

// Diagramme rendern
const renderCharts = () => {
  const lineCanvas = document.getElementById('lineChart') as HTMLCanvasElement | null;
  const barCanvas = document.getElementById('barChart') as HTMLCanvasElement | null;

  if (!lineCanvas || !barCanvas) return;

  const labels = measurements.value.map(m => new Date(m.recorded_at).toLocaleDateString());

  const lineData = measurements.value.map(m => Number(m[selectedLineData.value?.value as keyof MachineMeasurement] ?? 0));
  const barData = measurements.value.map(m => Number(m[selectedBarData.value?.value as keyof MachineMeasurement] ?? 0));

  // Daten-Objekte explizit definieren
  const lineChartData = {
    labels,
    datasets: [{
      label: selectedLineData.value?.label || '',
      data: lineData,
      borderColor: 'blue',
      borderWidth: 2,
      fill: false
    }]
  };

  const barChartData = {
    labels,
    datasets: [{
      label: selectedBarData.value?.label || '',
      data: barData,
      backgroundColor: 'purple',
      borderWidth: 1
    }]
  };

  // Falls Diagramme bereits existieren -> zerstören
  if (lineChart) lineChart.destroy();
  if (barChart) barChart.destroy();

  // Erstelle neue Diagramme
  lineChart = new Chart(lineCanvas.getContext('2d')!, { type: 'line', data: lineChartData });
  barChart = new Chart(barCanvas.getContext('2d')!, { type: 'bar', data: barChartData });
};

// Watcher für Diagramme
watch([selectedLineData, selectedBarData], renderCharts)

// Cleanup
onBeforeUnmount(() => {
  if (lineChart) lineChart.destroy()
  if (barChart) barChart.destroy()
})

// Init
onMounted(async () => {
  await fetchMachineDetails()
  await fetchMeasurements()
})
</script>
