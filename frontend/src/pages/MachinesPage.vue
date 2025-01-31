<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Maschinenverwaltung</h3>
    <div class="row q-col-gutter-lg">
      <!-- Maschinenliste -->
      <div class="col-12 col-sm-6 col-md-4" v-for="(machine, index) in machines" :key="machine.id">
        <Card>
          <template #title>
            {{ machine.name }}
          </template>
          <template #content>
            <p>Status: {{ machine.status }}</p>
          </template>
          <template #icon>
            <q-btn flat dense round color="white" icon="more_vert" @click="toggleMenu(index)" />
            <q-menu anchor="bottom right" self="top right" :offset="[0, 5]">
              <q-list>
                <q-item clickable v-close-popup @click="editMachine(index)">
                  <q-item-section>Bearbeiten</q-item-section>
                </q-item>
                <q-item clickable v-close-popup @click="confirmDelete(index)">
                  <q-item-section>Löschen</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </template>
        </Card>
      </div>

      <!-- Card für Hinzufügen -->
      <div class="col-12 col-sm-6 col-md-4">
        <Card>
          <template #content>
            <div class="flex flex-center">
              <Button class="btn btn-flat text-dark rounded" color="white" @click="showAddMachineModal = true">
                <i class="material-icons text-h5 text-dark">add</i>
              </Button>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Modal für neue Maschine -->
    <MachineModal :showModal="showAddMachineModal" @close="showAddMachineModal = false" @submit="addMachine" />

    <!-- Modal für Maschinenbearbeitung -->
    <MachineModal :showModal="showEditMachineModal" :machineToEdit="machineToEdit" @close="closeEditModal" @submit="updateMachine" />

    <!-- Löschdialog -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Maschine löschen</div>
        </q-card-section>
        <q-card-section> Bist du sicher, dass du diese Maschine löschen möchtest? </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Abbrechen" color="primary" @click="showDeleteDialog = false" />
          <q-btn flat label="Löschen" color="negative" @click="deleteMachine(selectedMachineIndex)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import Card from 'src/components/BaseCard.vue'
import Button from 'src/components/BaseButton.vue'
import MachineModal from 'src/components/modals/MachineModal.vue'

interface Machine {
  id: number
  name: string
  status: string
}

const machines = ref<Machine[]>([])
const showAddMachineModal = ref(false)
const showEditMachineModal = ref(false)
const showDeleteDialog = ref(false)
const selectedMachineIndex = ref<number | null>(null)
const machineToEdit = ref<Machine | null>(null)
const menuState = ref<boolean[]>([])

const toggleMenu = (index: number) => {
  menuState.value = machines.value.map((_, i) => (i === index ? !menuState.value[index] : false))
}

const editMachine = (index: number) => {
  machineToEdit.value = machines.value[index] || null
  showEditMachineModal.value = true
}

const closeEditModal = () => {
  showEditMachineModal.value = false
  machineToEdit.value = null
}

const updateMachine = async (updatedMachine: { name: string; status: string }) => {
  if (!machineToEdit.value) return
  try {
    const response = await api.put(`/machines/update/${machineToEdit.value.id}/`, updatedMachine)
    const updatedIndex = machines.value.findIndex((m) => m.id === machineToEdit.value?.id)
    if (updatedIndex !== -1) {
      machines.value[updatedIndex] = { ...machines.value[updatedIndex], ...response.data }
    }
    closeEditModal()
  } catch (error) {
    console.error('Fehler beim Aktualisieren der Maschine:', error)
  }
}

const confirmDelete = (index: number) => {
  selectedMachineIndex.value = index
  showDeleteDialog.value = true
}

const deleteMachine = async (index: number | null) => {
  if (index === null || index < 0 || index >= machines.value.length) return
  const machine = machines.value[index]
  if (!machine) return
  try {
    await api.delete(`/machines/delete/${machine.id}/`)
    machines.value.splice(index, 1)
    menuState.value.splice(index, 1)
    showDeleteDialog.value = false
  } catch (error) {
    console.error('Fehler beim Löschen der Maschine:', error)
  }
}

const fetchMachines = async () => {
  try {
    const response = await api.get('/machines/')
    machines.value = response.data
    menuState.value = Array(machines.value.length).fill(false)
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinen:', error)
  }
}

const addMachine = async (machineData: { name: string; status: string }) => {
  try {
    const response = await api.post('/machines/add/', machineData)
    machines.value.push(response.data)
    menuState.value.push(false)
    showAddMachineModal.value = false
  } catch (error) {
    console.error('Fehler beim Hinzufügen einer neuen Maschine:', error)
  }
}

onMounted(fetchMachines)
</script>
