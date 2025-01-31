<template>
  <q-page class="q-pa-md">
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Details für Maschine: {{ machine.name }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Zugewiesenes Feld:</strong> {{ machine.assigned_field?.name || 'Keins' }}</p>
        <p><strong>Status:</strong> {{ machine.status }}</p>
        <p><strong>Kategorie:</strong> {{ machine.category }}</p>
        <p><strong>Aktuell zugewiesen an:</strong> {{ machine.assigned_employee?.first_name || 'Keiner' }}</p>
      </q-card-section>

      <!-- Maschinenmesswerte -->
      <q-card-section>
        <h4>Letzte Maschinenmesswerte</h4>
        <q-table
          :rows="machineMeasurements"
          :columns="measurementColumns"
          row-key="id"
          dense
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { api } from "boot/axios"

const route = useRoute()
const router = useRouter()
const machineId = String(route.params.id)

interface Employee {
  first_name: string;
  // Add other properties if needed
}

const machine = ref<{
  id: number;
  name: string;
  status: string;
  category: string;
  assigned_field: { name: string } | null;
  assigned_employee: Employee | null;
}>({
  id: 0,
  name: "",
  status: "",
  assigned_field: null,
  assigned_employee: null,
  category: ""
})

const machineMeasurements = ref([])

const measurementColumns = [
  { name: "recorded_at", label: "Zeitpunkt", align: "left" as const, field: "recorded_at", sortable: true },
  { name: "fuel_level", label: "Tankfüllstand (%)", align: "left" as const, field: "fuel_level", sortable: true },
  { name: "engine_temperature", label: "Motortemp. (°C)", align: "left" as const, field: "engine_temperature", sortable: true },
  { name: "oil_level", label: "Ölstand (%)", align: "left" as const, field: "oil_level", sortable: true },
  { name: "rpm", label: "U/min", align: "left" as const, field: "rpm", sortable: true }
]

const fetchMachineDetails = async () => {
  try {
    const response = await api.get(`/machines/${machineId}/`)
    machine.value = response.data
  } catch (error) {
    console.error("Fehler beim Abrufen der Maschinendetails:", error)
    await router.push("/machines")
  }
}

const fetchMachineMeasurements = async () => {
  try {
    const response = await api.get(`/machines/${machineId}/measurements/`)
    machineMeasurements.value = response.data
  } catch (error) {
    console.error("Fehler beim Abrufen der Maschinenmesswerte:", error)
  }
}

const goBack = async () => {
  await router.push("/machines")
}

onMounted(async () => {
  await fetchMachineDetails()
  await fetchMachineMeasurements()
})
</script>
