<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="machineToEdit">Maschine bearbeiten</h4>
        <h4 v-else>Neue Maschine erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input v-model="machineData.name" label="Maschinenname" filled />
        <q-input v-model="machineData.serial_number" label="Seriennummer" filled />
        <q-input v-model="machineData.year_of_manufacture" label="Baujahr" type="number" filled />

        <q-select v-model="machineData.status" :options="statusOptions" label="Status" filled />
        <q-select
          v-model="machineData.category"
          :options="categoryOptions"
          label="Kategorie"
          filled
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn
          color="primary"
          :label="machineToEdit ? 'Speichern' : 'Erstellen'"
          @click="submitMachine"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, computed, watch } from 'vue'
import type { PropType } from 'vue'

const emit = defineEmits(['close', 'submit'])
const { showModal, machineToEdit } = defineProps({
  showModal: Boolean,
  machineToEdit: {
    type: Object as PropType<{
      name: string
      serial_number: string
      year_of_manufacture: number
      status: string
      category: string
    } | null>,
    default: null,
  },
})

const localShowModal = computed({
  get: () => showModal,
  set: (value) => {
    if (!value) emit('close')
  },
})

const statusOptions = ['In Betrieb', 'Wartung erforderlich', 'Defekt']
const categoryOptions = ['Traktor', 'Mähdrescher', 'Anhänger', 'Zubehör', 'Saatmaschine']

const machineData = ref<{
  name: string
  serial_number: string
  year_of_manufacture: number | null
  status: string
  category: string
}>({
  name: '',
  serial_number: '',
  year_of_manufacture: null,
  status: 'In Betrieb',
  category: 'Traktor',
})

watch(
  () => machineToEdit,
  (newMachine) => {
    if (newMachine) {
      machineData.value = { ...newMachine }
    } else {
      machineData.value = {
        name: '',
        serial_number: '',
        year_of_manufacture: null,
        status: 'In Betrieb',
        category: 'Traktor',
      }
    }
  },
  { immediate: true },
)

const submitMachine = () => {
  if (!machineData.value.name) {
    console.error('Maschinenname ist erforderlich!')
    return
  }
  if (!machineData.value.serial_number) {
    console.error('Seriennummer ist erforderlich!')
    return
  }
  if (
    !machineData.value.year_of_manufacture ||
    machineData.value.year_of_manufacture < 1900 ||
    machineData.value.year_of_manufacture > new Date().getFullYear()
  ) {
    console.error('Baujahr ist ungültig!')
    return
  }

  // Stelle sicher, dass `year_of_manufacture` als Zahl gesendet wird
  const formattedData = {
    ...machineData.value,
    year_of_manufacture: Number(machineData.value.year_of_manufacture), // Konvertiere zu Zahl
  }

  console.log('Gesendete Daten:', formattedData) // Debugging

  emit('submit', formattedData)
}

const cancel = () => {
  emit('close')
}
</script>
