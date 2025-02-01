<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="fieldToEdit">Feld bearbeiten</h4>
        <h4 v-else>Neues Feld erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input v-model="fieldData.name" label="Name" filled />
        <q-input v-model="fieldData.width" type="number" label="Breite (ha)" filled />
        <q-input v-model="fieldData.height" type="number" label="Höhe (ha)" filled />

        <!-- Dropdown für Saatgut-Auswahl -->
        <q-select
          v-model="fieldData.saat_name"
          :options="seedOptions"
          label="Saatgut auswählen"
          filled
          emit-value
          map-options
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn
          color="primary"
          :label="fieldToEdit ? 'Speichern' : 'Erstellen'"
          @click="submitField"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, computed, watch, onMounted } from 'vue'
import { api } from 'boot/axios'
import type { PropType } from 'vue'
import type { Field } from 'src/components/models'

const emit = defineEmits(['close', 'submit'])
const props = defineProps({
  showModal: Boolean,
  fieldToEdit: {
    type: Object as PropType<{
      name: string
      width: number
      height: number
      saat_name: string
    } | null>,
    default: null,
  },
})

const localShowModal = computed({
  get: () => props.showModal,
  set: (value) => {
    if (!value) emit('close')
  },
})

const fieldData = ref<Field>({
  id: 0,
  name: '',
  width: 0,
  height: 0,
  saat_name: '',
})

// Liste der verfügbaren Samen für die Auswahl
const seedOptions = ref<{ label: string; value: string }[]>([])

// API-Aufruf zur Saatgut-Liste
const fetchSeeds = async () => {
  try {
    const response = await api.get('/seeds/')
    seedOptions.value = response.data.map((seed: { id: number; name: string }) => ({
      label: seed.name,
      value: seed.name,
    }))
  } catch (error) {
    console.error('Fehler beim Abrufen der Saatgutliste:', error)
  }
}

// Aktualisiere die Felddaten, wenn `fieldToEdit` sich ändert
watch(
  () => props.fieldToEdit,
  (newField) => {
    if (newField) {
      fieldData.value = { id: fieldData.value.id, ...newField }
    } else {
      fieldData.value = { id: 0, name: '', width: 0, height: 0, saat_name: '' }
    }
  },
  { immediate: true },
)

// Lade die Saatgutliste, wenn das Modal geöffnet wird
onMounted(fetchSeeds)

const submitField = () => {
  if (!fieldData.value.width || !fieldData.value.height) {
    console.error('Breite und Höhe sind erforderlich!')
    return
  }
  emit('submit', { ...fieldData.value })
}

const cancel = () => {
  emit('close')
}
</script>
