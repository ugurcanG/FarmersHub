<template>
  <q-dialog :model-value="modelValue" @update:model-value="emit('update:modelValue', $event)">
    <q-card>
      <q-card-section>
        <div class="text-h6">Maschinen zuweisen</div>
      </q-card-section>

      <q-card-section>
        <q-list bordered separator>
          <q-item v-for="machine in machineOptions" :key="machine.id">
            <q-item-section avatar>
              <q-img v-if="machine.image_url" :src="machine.image_url" style="width: 50px; height: 50px;" />
            </q-item-section>
            <q-item-section>
              <q-checkbox v-model="selectedMachines" :val="machine.id" />
              <div>{{ machine.name }}</div>
              <div class="text-caption">
                {{ machine.category }} - {{ machine.status }} - {{ machine.operating_hours }} Betriebsstunden
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" color="primary" @click="closeModal" />
        <q-btn flat label="Speichern" color="primary" @click="saveMachineAssignments" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch } from 'vue'
import { api } from 'boot/axios'
import type { Machine } from 'src/components/models';

const props = defineProps({
  modelValue: Boolean,
  employeeId: Number,
  assignedMachines: Array as () => Machine[],
  machineOptions: Array as () => Machine[],
})

const emit = defineEmits(['update:modelValue', 'machinesUpdated'])

const selectedMachines = ref<number[]>([])

watch(
  () => props.employeeId,  // Beobachte, wenn sich die `employeeId` ändert
  () => {
    selectedMachines.value = (props.assignedMachines ?? []).map(machine => machine.id)
  },
  { immediate: true }  // Sofort beim Laden des Modals ausführen
)

const closeModal = () => {
  emit('update:modelValue', false)
}

const saveMachineAssignments = async () => {
  try {
    if (!props.employeeId) return

    await api.post('/machines/assign_machines/', {
      employee_id: props.employeeId,
      machine_ids: selectedMachines.value
    })

    emit('machinesUpdated')
    closeModal()
  } catch (error) {
    console.error('Fehler beim Speichern der Maschinenzuweisung:', error)
  }
}
</script>
