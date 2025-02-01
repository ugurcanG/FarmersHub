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

      <!-- Maschinen-Zuweisungs-Button jetzt in der "Aktionen"-Spalte -->
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn icon="map" color="green" flat round dense @click="openFieldModal(props.row)" />
          <q-btn icon="construction" color="primary" flat round dense @click="openMachineModal(props.row)" />
          <q-btn icon="edit" color="primary" flat round dense @click="editEmployee(props.row)" />
          <q-btn icon="delete" color="negative" flat round dense @click="confirmDelete(props.row.id)" />
        </q-td>
      </template>

      <!-- Maschinen anzeigen -->
      <template v-slot:body-cell-assigned_machines="props">
        <q-td :props="props">
          <span v-if="props.row.assigned_machines && props.row.assigned_machines.length">
            {{ props.row.assigned_machines.map((machine: Machine) => machine.name).join(', ') }}
          </span>
          <span v-else>Keine Maschinen zugewiesen</span>
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

    <!-- Modal für Maschinenzuweisung -->
    <MachineAssignmentModal
      :model-value="showMachineModal"
      @update:model-value="showMachineModal = $event"
      :employeeId="selectedEmployee?.id ?? 0"
      :assignedMachines="selectedEmployee?.assigned_machines || []"
      :machineOptions="machineOptions"
      @machinesUpdated="fetchEmployees"
    />

    <FieldAssignmentModal
  :model-value="showFieldModal"
  @update:model-value="showFieldModal = $event"
  :employeeId="selectedEmployeeForField?.id ?? 0"
  :fieldOptions="fieldOptions"
  @fieldAssigned="fetchEmployees"
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
            <q-btn flat label="Löschen" color="negative" @click="selectedEmployeeId !== null && deleteEmployee(selectedEmployeeId)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import EmployeeModal from 'src/components/modals/EmployeeModal.vue'
import MachineAssignmentModal from 'src/components/modals/MachineAssignmentModal.vue'
import FieldAssignmentModal from 'src/components/modals/FieldAssignmentModal.vue'
import type { Field, Machine, Employee } from 'src/components/models';

const showFieldModal = ref(false)
const fieldOptions = ref<Field[]>([])
const selectedEmployeeForField = ref<Employee | null>(null)

// Felder abrufen
const fetchFields = async () => {
  try {
    const response = await api.get('/fields/')
    fieldOptions.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error)
  }
}

// Feld-Zuweisungs-Modal öffnen
const openFieldModal = (employee: Employee) => {
  selectedEmployeeForField.value = employee
  showFieldModal.value = true
}

const employees = ref<Employee[]>([])
const machineOptions = ref<Machine[]>([])
const search = ref('')

// Computed property for filtered employees
const filteredEmployees = computed(() => {
  if (!search.value) {
    return employees.value
  }
  return employees.value.filter(employee =>
    `${employee.first_name} ${employee.last_name} ${employee.role}`.toLowerCase().includes(search.value.toLowerCase())
  )
})
const showAddEmployeeModal = ref(false)
const showEditEmployeeModal = ref(false)
const employeeToEdit = ref<Employee | null>(null)
const showDeleteDialog = ref(false)
const selectedEmployeeId = ref<number | null>(null)
const showMachineModal = ref(false)
const selectedEmployee = ref<Employee | null>(null)

// Spalten für die Tabelle
const columns: { name: string; label: string; field: string | ((row: Employee) => string); align: 'left' | 'center' | 'right'; sortable?: boolean }[] = [
  { name: 'first_name', label: 'Vorname', align: 'left', field: 'first_name', sortable: true },
  { name: 'last_name', label: 'Nachname', align: 'left', field: 'last_name', sortable: true },
  { name: 'role', label: 'Rolle', align: 'left', field: 'role', sortable: true },
  { name: 'assigned_field', label: 'Zugewiesenes Feld', align: 'left', field: (row: Employee) => row.assigned_field?.name || 'Kein Feld' },
  { name: 'assigned_machines', label: 'Maschinen', align: 'left', field: 'assigned_machines' },
  { name: 'actions', label: 'Aktionen', align: 'center', field: 'id' },
]

// **Mitarbeiter abrufen**
const fetchEmployees = async () => {
  try {
    const response = await api.get('/employees/')
    employees.value = response.data.map((employee: Employee) => ({
      ...employee,
      assigned_machines: employee.assigned_machines ?? [] // Falls null, leeres Array setzen
    }))
  } catch (error) {
    console.error('Fehler beim Abrufen der Mitarbeiter:', error)
  }
}

// Maschinen abrufen
const fetchMachines = async () => {
  try {
    const response = await api.get('/machines/')
    machineOptions.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Maschinen:', error)
  }
}

// Maschinen-Zuweisungs-Modal öffnen
const openMachineModal = (employee: Employee) => {
  console.log("Maschinen-Modal öffnen für:", employee)
  selectedEmployee.value = employee
  showMachineModal.value = true
}

// Neuen Mitarbeiter hinzufügen (fix: Modal schließt sich nach Hinzufügen)
const addEmployee = async (employeeData: { first_name: string; last_name: string; role: string }) => {
  try {
    const response = await api.post('/employees/add/', employeeData)
    if (response.data.employee) {
      employees.value.push(response.data.employee)
      showAddEmployeeModal.value = false // **Fix: Modal schließt sich jetzt**
    } else {
      console.error('Fehler: API antwortete mit unerwartetem Format', response.data)
    }
  } catch (error) {
    console.error('Fehler beim Hinzufügen eines Mitarbeiters:', error)
  }
}

// Mitarbeiter bearbeiten
const editEmployee = (employee: Employee) => {
  employeeToEdit.value = employee
  showEditEmployeeModal.value = true
}

// Modal für Mitarbeiterbearbeitung schließen
const closeEditModal = () => {
  showEditEmployeeModal.value = false
  employeeToEdit.value = null
}

// Mitarbeiter aktualisieren
const updateEmployee = async (updatedEmployee: { first_name: string; last_name: string; role: string }) => {
  if (!employeeToEdit.value) return

  try {
    const response = await api.put(`/employees/update/${employeeToEdit.value.id}/`, updatedEmployee)
    const index = employees.value.findIndex((e) => e.id === employeeToEdit.value?.id)
    if (index !== -1) employees.value[index] = { ...employees.value[index], ...response.data }

    showEditEmployeeModal.value = false
    employeeToEdit.value = null
    await fetchEmployees()
  } catch (error) {
    console.error('Fehler beim Aktualisieren des Mitarbeiters:', error)
  }
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

onMounted(async () => {
  await fetchEmployees()
  await fetchFields()
  await fetchMachines()
})
</script>
