<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Felder</h3>
    <div class="row q-col-gutter-lg">
      <!-- Bestehende Felder anzeigen -->
      <div class="col-12 col-sm-6 col-md-4" v-for="(field, index) in fields" :key="field.id">
        <Card>
          <template #title>
            <!-- Klickbarer Link -->
            <router-link
              :to="`/fields/${field.id}`"
              class="text-primary-style text-decoration-none"
            >
              {{ field.name }}
            </router-link>
          </template>
          <template #content>
            <div class="content-container">
              <p class="saat-info">
                Saatgut: <span>{{ field.saat_name || 'Kein Saatgut zugewiesen' }}</span>
              </p>
              <p class="size-info">Größe: {{ field.size }} ha</p>
            </div>
          </template>
          <template #icon>
            <q-btn
              flat
              dense
              round
              color="white"
              icon="more_vert"
              @click="toggleMenu(index)"
              ref="menuTrigger"
            />
            <q-menu anchor="bottom right" self="top right" :offset="[0, 5]">
              <q-list>
                <q-item clickable v-close-popup @click="editField(index)">
                  <q-item-section>Bearbeiten</q-item-section>
                </q-item>
                <q-item clickable v-close-popup @click="confirmDelete(index)">
                  <q-item-section>Löschen</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </template>
          <template #image>
            <div
              :class="{
                'bg-green-7': field.health_score != null && field.health_score >= 3,
                'bg-orange-5':
                  field.health_score != null && field.health_score >= 2 && field.health_score < 3,
                'bg-red-5': field.health_score != null && field.health_score < 2,
              }"
              style="width: 100px; height: 100px; transform: rotate(15deg); border: 1px"
            ></div>
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
                @click="showAddFieldModal = true"
              >
                <i class="material-icons text-h5 text-dark">add</i>
              </Button>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Modal für neues Feld erstellen -->
    <FieldModal
      :showModal="showAddFieldModal"
      @close="showAddFieldModal = false"
      @submit="addField"
    />

    <!-- Modal für Feld bearbeiten -->
    <FieldModal
      :showModal="showEditFieldModal"
      :fieldToEdit="fieldToEdit"
      @close="closeEditModal"
      @submit="updateField"
    />

    <!-- Löschdialog -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Feld löschen</div>
        </q-card-section>
        <q-card-section> Bist du sicher, dass du dieses Feld löschen möchtest? </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Abbrechen" color="primary" @click="showDeleteDialog = false" />
          <q-btn flat label="Löschen" color="negative" @click="deleteField(selectedFieldIndex)" />
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
import FieldModal from 'src/components/modals/FieldModal.vue'
import type { Field } from 'src/components/models'

const fields = ref<Field[]>([])
const showAddFieldModal = ref(false)
const showEditFieldModal = ref(false) // Zustand des Bearbeitungsmodals
const showDeleteDialog = ref(false) // Zustand für den Löschdialog
const selectedFieldIndex = ref<number | null>(null) // Index des zu löschenden Feldes
const fieldToEdit = ref<Field | null>(null) // Das Feld, das bearbeitet wird

// Menü für jedes Feld
const menuState = ref<boolean[]>([])

const toggleMenu = (index: number) => {
  menuState.value = fields.value.map((_, i) => (i === index ? !menuState.value[index] : false))
}

// Bearbeiten eines Feldes
const editField = (index: number) => {
  fieldToEdit.value = fields.value[index] || null
  showEditFieldModal.value = true // Bearbeitungsmodal öffnen
}

// Schließt das Bearbeitungsmodal
const closeEditModal = () => {
  showEditFieldModal.value = false
  fieldToEdit.value = null // Zurücksetzen
}

// Aktualisiert ein Feld
const updateField = async (updatedField: {
  name: string
  width: number
  height: number
  saat_name: string
}) => {
  if (!fieldToEdit.value) return

  try {
    const response = await api.put(`/fields/update/${fieldToEdit.value.id}/`, updatedField)
    console.log(`Feld ${fieldToEdit.value.id} erfolgreich aktualisiert`, response.data)

    const updatedIndex = fields.value.findIndex((f) => f.id === fieldToEdit.value?.id)
    if (updatedIndex !== -1) {
      fields.value[updatedIndex] = { ...fields.value[updatedIndex], ...response.data }
    }

    closeEditModal()
  } catch (error) {
    console.error('Fehler beim Aktualisieren des Feldes:', error)
  }
}

// Löschen eines Feldes bestätigen
const confirmDelete = (index: number) => {
  selectedFieldIndex.value = index
  showDeleteDialog.value = true
}

// Löscht ein Feld
const deleteField = async (index: number | null) => {
  if (index === null || index < 0 || index >= fields.value.length) return

  const field = fields.value[index]
  if (!field) return // Ensure field is defined
  try {
    await api.delete(`/fields/delete/${field.id}/`)
    fields.value.splice(index, 1) // Entferne das Feld aus der Liste
    menuState.value.splice(index, 1) // Entferne den Menüstatus
    showDeleteDialog.value = false // Schließe den Dialog
  } catch (error) {
    console.error('Fehler beim Löschen des Feldes:', error)
  }
}

// Felder laden
const fetchFields = async (): Promise<void> => {
  try {
    const response = await api.get('/fields/')
    fields.value = response.data
    menuState.value = Array(fields.value.length).fill(false)
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error)
  }
}

// Neues Feld erstellen
const addField = async (fieldData: {
  name: string
  width: number
  height: number
  saat_name: string
}) => {
  try {
    const response = await api.post('/fields/add/', fieldData)
    fields.value.push(response.data) // Das neue Feld zur Liste hinzufügen
    menuState.value.push(false) // Menüstatus initialisieren
    showAddFieldModal.value = false // Modal schließen
  } catch (error) {
    console.error('Fehler beim Hinzufügen eines neuen Feldes:', error)
  }
}

onMounted(fetchFields)
</script>

<style scoped>
.content-container {
  position: relative;
  bottom: 20px; /* Abstand zum unteren Rand */
  left: 10px; /* Abstand vom linken Rand */
  width: calc(100% - 20px); /* Damit es sich an die Card-Breite anpasst */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 8px;
  border-radius: 5px;
}

.saat-info,
.size-info {
  font-size: 1rem;
  color: white;
  margin: 2px 0;
}

a.text-primary-style {
  color: white; /* Quasar Primärfarbe */
  text-decoration: none; /* Entfernt Unterstrich */
  font-weight: bold; /* Fettschrift */
  font-size: large;
}

a.text-primary-style:hover {
  text-decoration: underline; /* Unterstrich beim Hover */
}
</style>
