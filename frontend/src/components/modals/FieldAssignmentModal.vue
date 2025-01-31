<template>
  <q-dialog :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <q-card>
      <q-card-section>
        <div class="text-h6">Feld zuweisen</div>
      </q-card-section>

      <q-card-section>
        <q-select
          v-model="selectedField"
          :options="fieldOptions"
          label="Feld auswählen"
          dense
          filled
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" color="primary" @click="closeModal" />
        <q-btn flat label="Speichern" color="primary" @click="saveFieldAssignment" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'
import { api } from 'boot/axios'

interface Field {
  id: number
  name: string
}

const props = defineProps({
  modelValue: Boolean,
  employeeId: Number,
  fieldOptions: Array as () => Field[],
})

const emit = defineEmits(['update:modelValue', 'fieldAssigned'])

const selectedField = ref<number | null>(null)

const closeModal = () => {
  emit('update:modelValue', false)
}

const saveFieldAssignment = async () => {
  try {
    if (!props.employeeId || !selectedField.value) return

    await api.post('/employees/assign_field/', {
      employee_id: props.employeeId,
      field_id: selectedField.value
    })

    emit('fieldAssigned')
    closeModal()
  } catch (error) {
    console.error('Fehler beim Speichern der Feldzuweisung:', error)
  }
}
</script>
