<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="machineToEdit">Maschine bearbeiten</h4>
        <h4 v-else>Neue Maschine erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input v-model="machineData.name" label="Maschinenname" filled />
        <q-select
          v-model="machineData.status"
          :options="statusOptions"
          label="Status"
          filled
        />
        <q-select
          v-model="machineData.category"
          :options="categoryOptions"
          label="Kategorie"
          filled
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn color="primary" :label="machineToEdit ? 'Speichern' : 'Erstellen'" @click="submitMachine" />
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
    type: Object as PropType<{ name: string; status: string; category: string } | null>,
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

const machineData = ref({
  name: '',
  status: 'In Betrieb',
  category: 'Traktor'
})

watch(
  () => machineToEdit,
  (newMachine) => {
    if (newMachine) {
      machineData.value = { ...newMachine }
    } else {
      machineData.value = { name: '', status: 'In Betrieb', category: 'Traktor' }
    }
  },
  { immediate: true }
)

const submitMachine = () => {
  if (!machineData.value.name) {
    console.error('Maschinenname ist erforderlich!')
    return
  }
  emit('submit', { ...machineData.value })
}

const cancel = () => {
  emit('close')
}
</script>
