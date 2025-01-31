<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Mitarbeiterverwaltung</h3>

    <!-- Suchfeld -->
    <q-input v-model="search" filled dense debounce="300" placeholder="Mitarbeiter suchen..." class="q-mb-md">
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>

    <!-- Tabelle -->
    <q-table
      :rows="filteredEmployees"
      :columns="columns"
      row-key="id"
      dense
      flat
      bordered
      no-data-label="Keine Mitarbeiter gefunden"
    >
      <template v-slot:top-right>
        <q-btn color="primary" label="Mitarbeiter hinzufügen" @click="showAddEmployeeModal = true" />
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn icon="edit" color="primary" flat round dense @click="editEmployee(props.row)" />
          <q-btn icon="delete" color="negative" flat round dense @click="confirmDelete(props.row.id)" />
        </q-td>
      </template>
    </q-table>

    <!-- Modal für neue Mitarbeiter -->
    <EmployeeModal
      :showModal="showAddEmployeeModal"
      @close="showAddEmployeeModal = false"
      @submit="addEmployee"
    />

    <!-- Modal für Mitarbeiterbearbeitung -->
    <EmployeeModal
      :showModal="showEditEmployeeModal"
      :employeeToEdit="employeeToEdit"
      @close="closeEditModal"
      @submit="updateEmployee"
    />

    <!-- Löschdialog -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Mitarbeiter löschen</div>
        </q-card-section>
        <q-card-section> Bist du sicher, dass du diesen Mitarbeiter löschen möchtest? </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Abbrechen" color="primary" @click="showDeleteDialog = false" />
          <q-btn flat label="Löschen" color="negative" @click="deleteEmployee(selectedEmployeeId)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import EmployeeModal from 'src/components/modals/EmployeeModal.vue'

interface Employee {
  id: number
  first_name: string
  last_name: string
  role: string
}

const employees = ref<Employee[]>([])
const search = ref('')
const showAddEmployeeModal = ref(false)
const showEditEmployeeModal = ref(false)
const showDeleteDialog = ref(false)
const selectedEmployeeId = ref<number | null>(null)
const employeeToEdit = ref<Employee | null>(null)

// Tabelle-Spalten
const columns = [
  { name: 'first_name', label: 'Vorname', align: 'left' as const, field: 'first_name', sortable: true },
  { name: 'last_name', label: 'Nachname', align: 'left' as const, field: 'last_name', sortable: true },
  { name: 'role', label: 'Rolle', align: 'left' as const, field: 'role', sortable: true },
  { name: 'actions', label: 'Aktionen', align: 'center' as const, field: 'id' },
]

// Gefilterte Liste für die Suche
const filteredEmployees = computed(() =>
  employees.value.filter(
    (employee) =>
      employee.first_name?.toLowerCase().includes(search.value.toLowerCase()) ||
      employee.last_name?.toLowerCase().includes(search.value.toLowerCase()) ||
      employee.role?.toLowerCase().includes(search.value.toLowerCase())
  )
)

// Mitarbeiter abrufen
const fetchEmployees = async () => {
  try {
    const response = await api.get('/employees/')
    employees.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Mitarbeiter:', error)
  }
}

// Neuen Mitarbeiter hinzufügen
const addEmployee = async (employeeData: { first_name: string; last_name: string; role: string }) => {
  try {
    const response = await api.post('/employees/add/', employeeData)
    if (response.data.employee) {
      employees.value.push(response.data.employee)
    } else {
      console.error('Fehler: API antwortete mit unerwartetem Format', response.data)
    }
  } catch (error) {
    console.error('Fehler beim Hinzufügen eines Mitarbeiters:', error)
  } finally {
    showAddEmployeeModal.value = false
  }
}

// Mitarbeiter bearbeiten
const editEmployee = (employee: Employee) => {
  employeeToEdit.value = employee
  showEditEmployeeModal.value = true
}

// Mitarbeiter aktualisieren
const updateEmployee = async (updatedEmployee: { first_name: string; last_name: string; role: string }) => {
  if (!employeeToEdit.value) return

  try {
    const response = await api.put(`/employees/update/${employeeToEdit.value.id}/`, updatedEmployee)
    const index = employees.value.findIndex((e) => e.id === employeeToEdit.value?.id)
    if (index !== -1) employees.value[index] = { ...employees.value[index], ...response.data }

    closeEditModal()
  } catch (error) {
    console.error('Fehler beim Aktualisieren des Mitarbeiters:', error)
  }
}

// Modal schließen
const closeEditModal = () => {
  showEditEmployeeModal.value = false
  employeeToEdit.value = null
}

// Mitarbeiter löschen bestätigen
const confirmDelete = (id: number) => {
  selectedEmployeeId.value = id
  showDeleteDialog.value = true
}

// Mitarbeiter löschen
const deleteEmployee = async (id: number | null) => {
  if (!id) return

  try {
    await api.delete(`/employees/delete/${id}/`)
    employees.value = employees.value.filter((e) => e.id !== id)
    showDeleteDialog.value = false
  } catch (error) {
    console.error('Fehler beim Löschen des Mitarbeiters:', error)
  }
}

onMounted(fetchEmployees)
</script>
