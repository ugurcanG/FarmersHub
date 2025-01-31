<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Maschinenverwaltung</h3>
    <div class="row q-col-gutter-lg">
      <!-- Maschinenliste -->
      <div
        class="col-12 col-sm-6 col-md-4 text-white"
        v-for="(machine, index) in machines"
        :key="machine.id"
      >
        <Card>
          <template #title>
            <!-- Klickbarer Link zum Maschinen-Detail -->
            <router-link :to="`/machines/${machine.id}`" class="text-primary-style text-decoration-none">
              {{ machine.name }}
            </router-link>
          </template>
          <template #content>
            <div class="machine-card-content">
              <div class="image-container">
                <img :src="getMachineImage(machine.category)" class="machine-icon" />
              </div>
              <p><strong>Status:</strong> {{ machine.status }}</p>
              <p><strong>Kategorie:</strong> {{ machine.category }}</p>
            </div>
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
              <Button
                class="btn btn-flat text-dark rounded"
                color="white"
                @click="showAddMachineModal = true"
              >
                <i class="material-icons text-h5 text-dark">add</i>
              </Button>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Modal für neue Maschine -->
    <MachineModal
      :showModal="showAddMachineModal"
      @close="showAddMachineModal = false"
      @submit="addMachine"
    />

    <!-- Modal für Maschinenbearbeitung -->
    <MachineModal
      :showModal="showEditMachineModal"
      :machineToEdit="machineToEdit"
      @close="closeEditModal"
      @submit="updateMachine"
    />

    <!-- Löschdialog -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Maschine löschen</div>
        </q-card-section>
        <q-card-section> Bist du sicher, dass du diese Maschine löschen möchtest? </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Abbrechen" color="primary" @click="showDeleteDialog = false" />
          <q-btn
            flat
            label="Löschen"
            color="negative"
            @click="deleteMachine(selectedMachineIndex)"
          />
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
  category: string
  image_url: string
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

// Maschinen abrufen
const fetchMachines = async () => {
  try {
    const response = await api.get('/machines/')
    machines.value = response.data
    menuState.value = Array(machines.value.length).fill(false)
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinen:', error)
  }
}

// Maschine bearbeiten
const editMachine = (index: number) => {
  machineToEdit.value = machines.value[index] || null
  showEditMachineModal.value = true
}

// Modal schließen
const closeEditModal = () => {
  showEditMachineModal.value = false
  machineToEdit.value = null
}

// Maschine aktualisieren
const updateMachine = async (updatedMachine: {
  name: string
  status: string
  category: string
}) => {
  if (!machineToEdit.value) return
  try {
    await api.put(`/machines/update/${machineToEdit.value.id}/`, updatedMachine)
    await fetchMachines() // Aktualisierung der Maschinenliste nach Bearbeitung
    closeEditModal()
  } catch (error) {
    console.error('Fehler beim Aktualisieren der Maschine:', error)
  }
}

// Maschine löschen
const confirmDelete = (index: number) => {
  selectedMachineIndex.value = index
  showDeleteDialog.value = true
}

const deleteMachine = async (index: number | null) => {
  if (index === null || index < 0 || index >= machines.value.length) return
  try {
    const machine = machines.value[index]
    if (!machine) return
    await api.delete(`/machines/delete/${machine.id}/`)
    await fetchMachines() // Liste nach Löschen aktualisieren
    showDeleteDialog.value = false
  } catch (error) {
    console.error('Fehler beim Löschen der Maschine:', error)
  }
}

// Neue Maschine hinzufügen
const addMachine = async (machineData: { name: string; status: string; category: string }) => {
  try {
    await api.post('/machines/add/', machineData)
    await fetchMachines() // Liste nach Hinzufügen aktualisieren
    showAddMachineModal.value = false
  } catch (error) {
    console.error('Fehler beim Hinzufügen einer neuen Maschine:', error)
  }
}

// Maschinenbild basierend auf Kategorie abrufen
const getMachineImage = (category: string) => {
  const images: { [key: string]: string } = {
    Traktor:
      'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/traktor.webp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy90cmFrdG9yLndlYnAiLCJpYXQiOjE3MzgzMzQwMjIsImV4cCI6MTc2OTg3MDAyMn0.mwb-ZBpCsQGaIYbhrcNfq9C6-yn_e_R9VS_ri6alE0M',
    Mähdrescher:
      'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/maehdrescher.jpeg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy9tYWVoZHJlc2NoZXIuanBlZyIsImlhdCI6MTczODMzMzk5NiwiZXhwIjoxNzY5ODY5OTk2fQ.2kINjKF6WkIAqGDSnnKY0C8gR4HwBoih00kriB24gK0',
    Anhänger:
      'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/anhaenger.jpeg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy9hbmhhZW5nZXIuanBlZyIsImlhdCI6MTczODMzMzk3NSwiZXhwIjoxNzY5ODY5OTc1fQ.oURIp8dyPg7wtBxTUQ7huABcyBfb5H6o5R5MivFYc9o',
    Zubehör:
      'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/zubehoer.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy96dWJlaG9lci5qcGciLCJpYXQiOjE3MzgzMzQwMzAsImV4cCI6MTc2OTg3MDAzMH0.lD4f4lLWYIOgsWicLb0tN8pq0Gd4RNd8MdfempW8E5U',
    Saatmaschine:
      'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/saatmaschine.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy9zYWF0bWFzY2hpbmUuanBnIiwiaWF0IjoxNzM4MzM0MDEyLCJleHAiOjE3Njk4NzAwMTJ9.FlZRuTAKPqpJyv24uoRMb3c9KgEyKwbJWXGEnNrQLgk',
  }
  return (
    images[category] ||
    'https://qbqnlcmndkrpwmdepmft.supabase.co/storage/v1/object/sign/machine-images/default.webp?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJtYWNoaW5lLWltYWdlcy9kZWZhdWx0LndlYnAiLCJpYXQiOjE3MzgzMzM5ODcsImV4cCI6MTc2OTg2OTk4N30.x1rNNhTyF4j-5EArDyWLAN42NQHgBFKLM2mmj3AwBEM'
  )
}

onMounted(fetchMachines)
</script>

<style>
.machine-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start; /* Inhalte nach oben schieben */
  text-align: center;
  height: 100%;
  position: relative; /* Für absolute Positionierung */
  top: -20px;
}

.image-container {
  position: relative;
  top: -20px; /* Bild nach oben verschieben */
  width: 100%;
  display: flex;
  justify-content: center;
}

.machine-icon {
  width: 70%;
  max-width: 160px;
  height: auto;
  display: block;
}

a.text-primary-style {
  color: white;
  text-decoration: none;
  font-weight: bold;
  font-size: large;
}

a.text-primary-style:hover {
  text-decoration: underline;
}
</style>
