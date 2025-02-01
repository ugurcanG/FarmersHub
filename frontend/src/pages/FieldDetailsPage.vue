<template>
  <q-page class="q-pa-md">
    <!-- Basisdetails -->
    <EntityDetails
  title="Feld-Details"
  :details="field"
  :labels="{
    name: 'Feldname',
    size: 'Größe (ha)',
    saat__name: 'Saatgut',
    created_at: 'Erstellt am',
    health_score: 'Health Score'
  }"
  :formatMap="{
    created_at: formatDateTime
  }"
>
  <template #actions>
    <q-btn flat label="Zurück" color="primary" @click="goBack" />
  </template>
</EntityDetails>

<!-- Messwerte -->
<EntityMeasurements
  title="Messwerte"
  :measurements="fieldMeasurements"
  :columns="columns"
  :fetchMeasurements="fetchMeasurements"
/>

    <!-- Diagramme -->
    <EntityCharts
      title="Messwerte-Analyse"
      :labels="labels"
      :formattedData="formattedData"
      :chartOptions="chartOptions"
    />

    <!-- Chat Drawer -->
    <ChatDrawer v-model:chatDrawerOpen="chatDrawerOpen" />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from 'boot/axios';
import type { FieldMeasurement } from 'src/components/models';
import EntityMeasurements from 'src/components/shared/EntityMeasurements.vue';
import EntityCharts from 'src/components/shared/EntityCharts.vue';
import EntityDetails from 'src/components/shared/EntityDetails.vue';
import ChatDrawer from 'src/components/shared/ChatDrawer.vue';
import { formatDateTime } from 'src/utils/dateUtils';

const chatDrawerOpen = ref(false);

const field = ref({
  id: 0,
  name: '',
  size: 0,
  created_at: '',
  saat__name: null,
  health_score: null,
});

const fieldMeasurements = ref<FieldMeasurement[]>([]);
  const columns = [
  {
    name: 'created_at',
    label: 'Datum',
    field: 'created_at',
    align: 'left' as const,
    sortable: true,
    format: (val: unknown) => (typeof val === 'string' ? formatDateTime(val) : 'Unbekannt')
  },
  { name: 'temperature', label: 'Temperatur (°C)', field: 'temperature', align: 'left' as const, sortable: true },
  { name: 'humidity', label: 'Luftfeuchtigkeit (%)', field: 'humidity', align: 'left' as const, sortable: true },
  { name: 'soil_moisture', label: 'Bodenfeuchte (%)', field: 'soil_moisture', align: 'left' as const, sortable: true },
  { name: 'nutrients_level', label: 'Nährstoffe', field: 'nutrients_level', align: 'left' as const, sortable: true },
  { name: 'health_score', label: 'Health Score', field: 'health_score', align: 'left' as const, sortable: true },
];

const labels = ref<string[]>([]);
const formattedData = ref<{ [key: string]: number }[]>([]);
const chartOptions = ref([
  { label: 'Temperatur (°C)', value: 'temperature' },
  { label: 'Luftfeuchtigkeit (%)', value: 'humidity' },
  { label: 'Bodenfeuchte (%)', value: 'soil_moisture' },
  { label: 'Nährstoffe', value: 'nutrients_level' },
  { label: 'Health Score', value: 'health_score' },
]);

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
    fieldMeasurements.value = response.data;
  } catch (error) {
    console.error('Fehler beim Abrufen der Messwerte:', error);
  }
};

watch(fieldMeasurements, () => {
  labels.value = fieldMeasurements.value.map((m) => new Date(m.created_at).toLocaleDateString());

  formattedData.value = fieldMeasurements.value.map((m) => ({
    temperature: m.temperature || 0,
    humidity: m.humidity || 0,
    soil_moisture: m.soil_moisture || 0,
    nutrients_level: m.nutrients_level || 0,
    health_score: m.health_score || 0,
  }));
});

const goBack = async () => {
  await router.push('/fields');
};

onMounted(async () => {
  await fetchFieldDetails();
  await fetchMeasurements();
});
</script>
