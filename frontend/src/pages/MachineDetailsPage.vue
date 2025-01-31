<template>
  <q-page class="q-pa-md">
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Details für Maschine: {{ machine.name }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Status:</strong> {{ machine.status }}</p>
        <p><strong>Kategorie:</strong> {{ machine.category }}</p>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'

const route = useRoute()
const router = useRouter()
const machineId = String(route.params.id)

const machine = ref({
  id: 0,
  name: '',
  status: '',
  category: '',
})

const fetchMachineDetails = async () => {
  try {
    const response = await api.get(`/machines/${machineId}/`)
    machine.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinendetails:', error)
    await router.push('/machines')
  }
}

const goBack = async () => {
  await router.push('/machines')
}

onMounted(fetchMachineDetails)
</script>
