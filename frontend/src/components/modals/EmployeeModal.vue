<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="employeeToEdit">Mitarbeiter bearbeiten</h4>
        <h4 v-else>Neuen Mitarbeiter erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input v-model="employeeData.first_name" label="Vorname" filled />
        <q-input v-model="employeeData.last_name" label="Nachname" filled />
        <q-select v-model="employeeData.role" :options="roles" label="Rolle" filled />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn color="primary" :label="employeeToEdit ? 'Speichern' : 'Erstellen'" @click="submitEmployee" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, computed, watch } from 'vue'
import type { PropType } from 'vue'

const emit = defineEmits(['close', 'submit'])
const { showModal, employeeToEdit } = defineProps({
  showModal: Boolean,
  employeeToEdit: Object as PropType<{ first_name: string; last_name: string; role: string } | null>,
})

const localShowModal = computed({
  get: () => showModal,
  set: (value) => {
    if (!value) emit('close')
  },
})

const roles = ['Landwirt', 'Mechaniker', 'Manager']
const employeeData = ref({ first_name: '', last_name: '', role: 'Landwirt' })

watch(
  () => employeeToEdit,
  (newEmployee) => {
    employeeData.value = newEmployee
      ? { ...newEmployee }
      : { first_name: '', last_name: '', role: 'Landwirt' }
  },
  { immediate: true },
)

const submitEmployee = () => {
  emit('submit', { ...employeeData.value })
}

const cancel = () => {
  emit('close')
}
</script>
