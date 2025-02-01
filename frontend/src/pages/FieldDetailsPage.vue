<template>
  <q-page class="q-pa-md">
    <!-- Basisdetails & Durchschnittswerte in zwei Spalten -->
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <!-- Linke Spalte: Feld-Details -->
          <div class="col-12 col-md-6">
            <h4 class="text-h6">Feld-Details</h4>
            <q-separator class="q-mb-md" />
            <q-table
              dense
              flat
              bordered
              hide-bottom
              :rows="Object.entries(fieldLabels)"
              :columns="[
                {
                  name: 'label',
                  label: '',
                  align: 'left',
                  field: (row) => row[1],
                  style: 'font-weight: bold;',
                },
                {
                  name: 'value',
                  label: '',
                  align: 'left',
                  field: (row) => formatValue((field as Record<string, unknown>)[row[0]], row[0]),
                },
              ]"
            />
          </div>

          <!-- Rechte Spalte: Durchschnittswerte -->
          <div class="col-12 col-md-6">
            <h4 class="text-h6">Durchschnittswerte</h4>
            <q-separator class="q-mb-md" />
            <q-table
              dense
              flat
              bordered
              hide-bottom
              :rows="Object.entries(averageLabels)"
              :columns="[
                {
                  name: 'label',
                  label: '',
                  align: 'left',
                  field: (row) => row[1],
                  style: 'font-weight: bold;',
                },
                {
                  name: 'value',
                  label: '',
                  align: 'left',
                  field: (row) => formatValue(averageValues[row[0]], row[0]),
                },
              ]"
            />
          </div>
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>

    <!-- Maschinen-Tabelle -->
    <InfoCard title="Zugewiesene Maschinen">
      <DataTable :rows="fieldMachines" :columns="machineColumns" />
    </InfoCard>

    <!-- Mitarbeiter-Tabelle -->
    <InfoCard title="Zugewiesene Mitarbeiter">
      <DataTable :rows="fieldEmployees" :columns="employeeColumns" />
    </InfoCard>

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
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'
import type { FieldMeasurement, Field } from 'src/components/models'
import EntityMeasurements from 'src/components/shared/EntityMeasurements.vue'
import EntityCharts from 'src/components/shared/EntityCharts.vue'
import ChatDrawer from 'src/components/shared/ChatDrawer.vue'
import InfoCard from 'src/components/shared/InfoCard.vue'
import DataTable from 'src/components/shared/DataTable.vue'
import { formatDateTime } from 'src/utils/dateUtils'

const chatDrawerOpen = ref(false)

const field = ref<Field>({
  id: 0,
  name: '',
  width: 0,
  height: 0,
  size: 0,
  saat_name: '',
  created_at: '',
  health_score: 0,
})

const fieldMeasurements = ref<FieldMeasurement[]>([])
const fieldMachines = ref<{ id: number; name: string; type: string }[]>([])
const fieldEmployees = ref<{ id: number; name: string; role: string }[]>([])

const fieldLabels: Record<string, string> = {
  name: 'Feldname',
  size: 'Größe (ha)',
  saat_name: 'Saatgut',
  created_at: 'Erstellt am',
  health_score: 'Health Score',
}

const averageLabels: Record<string, string> = {
  avg_temperature: 'Ø Temperatur (°C)',
  avg_humidity: 'Ø Luftfeuchtigkeit (%)',
  avg_soil_moisture: 'Ø Bodenfeuchte (%)',
  avg_nutrients_level: 'Ø Nährstoffe',
}

const formatValue = (value: unknown, key?: string): string => {
  if (key === 'created_at' && typeof value === 'string') {
    return formatDateTime(value) // 💡 Wendet die Formatierungsfunktion an
  }

  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
    return String(value)
  }

  if (value === null || value === undefined) return 'Nicht verfügbar'

  if (Array.isArray(value)) return value.join(', ') // Arrays als CSV-Format anzeigen

  if (typeof value === 'object') return '[Objekt]' // Verhindert [object Object] Ausgabe

  return 'Nicht verfügbar'
}

const columns = [
  {
    name: 'created_at',
    label: 'Datum',
    field: 'created_at',
    align: 'left' as const,
    sortable: true,
    format: (val: unknown) => (typeof val === 'string' ? formatDateTime(val) : 'Unbekannt'),
  },
  {
    name: 'temperature',
    label: 'Temperatur (°C)',
    field: 'temperature',
    align: 'left' as const,
    sortable: true,
  },
  {
    name: 'humidity',
    label: 'Luftfeuchtigkeit (%)',
    field: 'humidity',
    align: 'left' as const,
    sortable: true,
  },
  {
    name: 'soil_moisture',
    label: 'Bodenfeuchte (%)',
    field: 'soil_moisture',
    align: 'left' as const,
    sortable: true,
  },
  {
    name: 'nutrients_level',
    label: 'Nährstoffe',
    field: 'nutrients_level',
    align: 'left' as const,
    sortable: true,
  },
  {
    name: 'health_score',
    label: 'Health Score',
    field: 'health_score',
    align: 'left' as const,
    sortable: true,
  },
]

const machineColumns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' as const },
  { name: 'name', label: 'Maschinenname', field: 'name', align: 'left' as const },
  { name: 'type', label: 'Maschinentyp', field: 'type', align: 'left' as const },
]

const employeeColumns = [
  { name: 'id', label: 'ID', field: 'id', align: 'left' as const },
  { name: 'name', label: 'Mitarbeitername', field: 'name', align: 'left' as const },
  { name: 'role', label: 'Rolle', field: 'role', align: 'left' as const },
]

const labels = ref<string[]>([])
const formattedData = ref<{ [key: string]: number }[]>([])
const chartOptions = ref([
  { label: 'Temperatur (°C)', value: 'temperature' },
  { label: 'Luftfeuchtigkeit (%)', value: 'humidity' },
  { label: 'Bodenfeuchte (%)', value: 'soil_moisture' },
  { label: 'Nährstoffe', value: 'nutrients_level' },
  { label: 'Health Score', value: 'health_score' },
])

const route = useRoute()
const router = useRouter()
const fieldId = String(route.params.id)

const fetchFieldDetails = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/`)

    field.value = response.data

    await fetchMachinesForField(fieldId)
await fetchEmployeesForField(fieldId)


  } catch (error) {
    console.error('Fehler beim Abrufen der Felddetails:', error)
    await router.push('/fields')
  }
}

const fetchMachinesForField = async (fieldId: string) => {
  try {
    const response = await api.get(`/machines/by-field/${fieldId}/`)
    fieldMachines.value = response.data || []
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinen für das Feld:', error)
  }
}

const fetchEmployeesForField = async (fieldId: string) => {
  try {
    const response = await api.get(`/employees/by-field/${fieldId}/`)
    fieldEmployees.value = response.data || []
  } catch (error) {
    console.error('Fehler beim Abrufen der Mitarbeiter für das Feld:', error)
  }
}


const fetchMeasurements = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/measurements/`)
    fieldMeasurements.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Messwerte:', error)
  }
}

watch(fieldMeasurements, () => {
  labels.value = fieldMeasurements.value.map((m) => new Date(m.created_at).toLocaleDateString())

  formattedData.value = fieldMeasurements.value.map((m) => ({
    temperature: m.temperature || 0,
    humidity: m.humidity || 0,
    soil_moisture: m.soil_moisture || 0,
    nutrients_level: m.nutrients_level || 0,
    health_score: m.health_score || 0,
  }))
})

const averageValues = computed<Record<string, string>>(() => {
  if (!fieldMeasurements.value.length) return {}
  const sum = (key: keyof FieldMeasurement) =>
    fieldMeasurements.value.reduce((acc, m) => acc + (Number(m[key]) || 0), 0) /
    fieldMeasurements.value.length

  return {
    avg_temperature: sum('temperature').toFixed(2),
    avg_humidity: sum('humidity').toFixed(2),
    avg_soil_moisture: sum('soil_moisture').toFixed(2),
    avg_nutrients_level: sum('nutrients_level').toFixed(2),
  }
})

const goBack = async () => {
  await router.push('/fields')
}

onMounted(async () => {
  await fetchFieldDetails()
  await fetchMeasurements()
})
</script>
