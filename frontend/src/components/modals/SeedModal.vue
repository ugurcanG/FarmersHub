<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="seedToEdit">Saatgut bearbeiten</h4>
        <h4 v-else>Neues Saatgut hinzufügen</h4>
      </q-card-section>

      <q-card-section>
        <q-input v-model="seedData.name" label="Saatgutname" filled />
        <q-input v-model="seedData.mass_kg" label="Masse (kg)" type="number" filled />
        <q-input v-model="seedData.pref_temperature" label="Bevorzugte Temperatur (°C)" type="number" filled />
        <q-input v-model="seedData.pref_humidity" label="Bevorzugte Luftfeuchte (%)" type="number" filled />
        <q-input v-model="seedData.pref_soil_moisture" label="Bevorzugte Bodenfeuchte (%)" type="number" filled />
        <q-input v-model="seedData.pref_nutrient_level" label="Nährstofflevel" type="number" filled />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn
          color="primary"
          :label="seedToEdit ? 'Speichern' : 'Erstellen'"
          @click="submitSeed"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed, watch } from 'vue'
import type { Seed } from 'src/components/models'

const emit = defineEmits(['close', 'submit'])

const props = defineProps({
  showModal: Boolean,
  seedToEdit: Object as () => Seed | null, // Korrekte Typisierung
})

const localShowModal = computed({
  get: () => props.showModal,
  set: (value) => {
    if (!value) emit('close')
  },
})

// 🌱 Standardwerte für das Formular
const defaultSeed: Seed = {
  name: '',
  mass_kg: null,
  pref_temperature: null,
  pref_humidity: null,
  pref_soil_moisture: null,
  pref_nutrient_level: null,
}

// 🌱 Reaktiver Zustand für das bearbeitete Saatgut
const seedData = ref<Seed>({ ...defaultSeed })

// 🌍 Aktualisiere seedData, wenn seedToEdit sich ändert
watch(
  () => props.seedToEdit,
  (newSeed) => {
    seedData.value = newSeed ? { ...newSeed } : { ...defaultSeed }
  },
  { immediate: true }
)

// 📩 Saatgut speichern
const submitSeed = () => {
  emit('submit', { ...seedData.value })
}

// ❌ Abbrechen
const cancel = () => {
  emit('close')
}
</script>
