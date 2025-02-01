<template>
  <q-page class="q-pa-md">
    <q-btn label="Neues Saatgut hinzufügen" color="primary" @click="openSeedDialog()" class="q-mb-md" />
    <!-- Saatgut-Tabelle mit Hinzufügen-Button -->
    <DataTable :rows="seeds" :columns="columns" @refresh="fetchSeeds">
      <template v-slot:top-right>
        <q-btn label="Neues Saatgut hinzufügen" color="primary" @click="openSeedDialog()" />
      </template>

      <!-- Benutzerdefinierter Slot für die Aktionsspalte -->
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat dense round icon="edit" color="blue" @click="openSeedDialog(props.row)" />
          <q-btn flat dense round icon="delete" color="red" @click="deleteSeed(props.row.id)" />
        </q-td>
      </template>
    </DataTable>

    <!-- Saatgut-Modal -->
    <SeedModal
      :showModal="isSeedDialogOpen"
      :seedToEdit="selectedSeed"
      @close="isSeedDialogOpen = false"
      @submit="handleSeedSubmit"
    />

    <!-- ChatDrawer für GPT Chat -->
    <ChatDrawer v-model:chatDrawerOpen="chatDrawerOpen" />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import DataTable from 'src/components/shared/DataTable.vue'
import ChatDrawer from 'src/components/shared/ChatDrawer.vue'
import SeedModal from 'src/components/modals/SeedModal.vue'
import type { Seed } from 'src/components/models'

// 🌱 State-Variablen
const chatDrawerOpen = ref(false)
const seeds = ref<Seed[]>([])

const isSeedDialogOpen = ref(false)
const selectedSeed = ref<Seed | null>(null)

// 📊 Tabellen-Spalten mit Aktionsspalte
const columns = [
  { name: 'name', label: 'Saatgutname', field: 'name', align: 'left' as const },
  { name: 'mass_kg', label: 'Masse (kg)', field: 'mass_kg', align: 'left' as const },
  { name: 'pref_temperature', label: 'Temp. (°C)', field: 'pref_temperature', align: 'left' as const },
  { name: 'pref_humidity', label: 'Feuchte (%)', field: 'pref_humidity', align: 'left' as const },
  { name: 'pref_soil_moisture', label: 'Bodenfeuchte (%)', field: 'pref_soil_moisture', align: 'left' as const },
  { name: 'pref_nutrient_level', label: 'Nährstoffe', field: 'pref_nutrient_level', align: 'left' as const },
  { name: 'actions', label: 'Aktionen', align: 'center' as const, field: 'actions' },
]

// 🌍 Saatgut abrufen
const fetchSeeds = async () => {
  try {
    const response = await api.get('/seeds/')
    seeds.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Saatgutsorten:', error)
  }
}

// ➕ Neues/Bearbeitetes Saatgut speichern
const openSeedDialog = (seed: Seed | null = null) => {
  selectedSeed.value = seed ? { ...seed } : null // Wenn kein Seed übergeben wird, bedeutet das "Neues Saatgut"
  isSeedDialogOpen.value = true
}

// 📩 Saatgut speichern (Neu oder Update)
const handleSeedSubmit = async (seed: Seed) => {
  try {
    if (selectedSeed.value?.id) {
      await api.put(`/seeds/update/${selectedSeed.value.id}/`, seed)
    } else {
      await api.post('/seeds/add/', seed)
    }
    isSeedDialogOpen.value = false
    await fetchSeeds()
  } catch (error) {
    console.error('Fehler beim Speichern des Saatguts:', error)
  }
}

// ❌ Saatgut löschen
const deleteSeed = async (seedId: number) => {
  if (!confirm('Möchtest du dieses Saatgut wirklich löschen?')) return
  try {
    await api.delete(`/seeds/delete/${seedId}/`)
    await fetchSeeds()
  } catch (error) {
    console.error('Fehler beim Löschen des Saatguts:', error)
  }
}

onMounted(fetchSeeds)
</script>
