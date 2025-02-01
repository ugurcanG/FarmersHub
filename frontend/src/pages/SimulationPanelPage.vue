<template>
  <q-page class="q-pa-md">
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Simulations-Panel</h3>
      </q-card-section>

      <q-card-section>
        <!-- Auswahl: Felder -->
        <q-select
          v-model="selectedField"
          :options="fieldOptions"
          label="Feld auswählen"
          outlined
          dense
          class="q-mb-md"
        />
        <q-btn color="primary" @click="generateFieldMeasurements" :disable="!selectedField">Feld-Messwerte generieren</q-btn>
      </q-card-section>

      <q-card-section>
        <!-- Auswahl: Maschinen -->
        <q-select
          v-model="selectedMachine"
          :options="machineOptions"
          label="Maschine auswählen"
          outlined
          dense
          class="q-mb-md"
        />
        <q-btn color="secondary" @click="generateMachineMeasurements" :disable="!selectedMachine">Maschinen-Messwerte generieren</q-btn>
      </q-card-section>

      <q-card-section v-if="message">
        <q-banner inline-actions class="bg-green text-white">
          {{ message }}
        </q-banner>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import type { AxiosError } from "axios";
import type { Field, Machine, ApiResponse } from 'src/components/models';

const selectedField = ref<{ label: string, value: number } | null>(null)
const selectedMachine = ref<{ label: string, value: number } | null>(null)
const fieldOptions = ref<Array<{ label: string, value: number }>>([])
const machineOptions = ref<Array<{ label: string, value: number }>>([])
const message = ref<string>('')

// Felder abrufen
const fetchFields = async () => {
  try {
    const response: ApiResponse<Field[]> = await api.get('/fields/')
    fieldOptions.value = response.data.map(field => ({
      label: field.name,
      value: field.id
    }))
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error)
  }
}

// Maschinen abrufen
const fetchMachines = async () => {
  try {
    const response: ApiResponse<Machine[]> = await api.get('/machines/')
    machineOptions.value = response.data.map(machine => ({
      label: machine.name,
      value: machine.id
    }))
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinen:', error)
  }
}

// API-Request zur Simulation der Feld-Messwerte
const generateFieldMeasurements = async (): Promise<void> => {
  try {
    const response: ApiResponse<{ message: string }> = await api.post('/simulation/generate_field_measurements/', {
      field_id: selectedField.value?.value
    })
    message.value = response.data.message
  } catch (error) {
    const axiosError = error as AxiosError<{ error: string }>;

    console.error(
      'Fehler beim Generieren von Messwerten:',
      axiosError.response?.data?.error || axiosError.message
    );

    message.value = axiosError.response?.data?.error || "Fehler bei der Messwert-Generierung!";
  }
}

// API-Request zur Simulation der Maschinen-Messwerte
const generateMachineMeasurements = async (): Promise<void> => {
  try {
    const response: ApiResponse<{ message: string }> = await api.post('/simulation/generate_machine_measurements/', {
      machine_id: selectedMachine.value?.value
    })
    message.value = response.data.message
  } catch (error) {
    const axiosError = error as AxiosError<{ error: string }>;

    console.error(
      'Fehler beim Generieren von Maschinenmesswerten:',
      axiosError.response?.data?.error || axiosError.message
    );

    message.value = axiosError.response?.data?.error || "Fehler bei der Maschinen-Messwert-Generierung!";
  }
}


onMounted(async () => {
  await fetchFields()
  await fetchMachines()
})
</script>
