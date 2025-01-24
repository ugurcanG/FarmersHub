<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Felder</h3>
    <div class="row q-col-gutter-lg">
      <div
        class="col-12 col-sm-6 col-md-4"
        v-for="(field, index) in fields"
        :key="field.id"
      >
        <Card :title="'Feld ' + field.id">
          <template #content>
            <div class="content-container">
              <p>Größe: {{ field.size }} ha</p>
              <p class="saat-info">
                Saatgut: <span>{{ field.saat__name || 'Kein Saatgut zugewiesen' }}</span>
              </p>
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
            <q-menu
              anchor="bottom right"
              self="top right"
              :offset="[0, 5]"
            >
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
              class="bg-green-5"
              style="width: 100px; height: 100px; transform: rotate(15deg);"
            ></div>
          </template>
        </Card>
      </div>

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

    <FieldModal
      :showModal="showAddFieldModal"
      @close="showAddFieldModal = false"
      @submit="addField"
    />

    <!-- Löschdialog -->
    <q-dialog v-model="showDeleteDialog">
      <q-card>
        <q-card-section>
          <div class="text-h6">Feld löschen</div>
        </q-card-section>
        <q-card-section>
          Bist du sicher, dass du dieses Feld löschen möchtest?
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Abbrechen" color="primary" @click="showDeleteDialog = false" />
          <q-btn flat label="Löschen" color="negative" @click="deleteField(selectedFieldIndex)" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios';
import Card from 'src/components/BaseCard.vue';
import Button from 'src/components/BaseButton.vue';
import FieldModal from 'src/components/modals/FieldModal.vue';

interface Field {
  id: number;
  size: number; // Größe des Feldes
  created_at: string;
  saat__name: string | null; // Name des Saatguts (falls vorhanden)
}

const fields = ref<Field[]>([]);
const showAddFieldModal = ref(false);
const showDeleteDialog = ref(false); // Dialogzustand für Löschen
const selectedFieldIndex = ref<number | null>(null); // Index des zu löschenden Feldes

const menuState = ref<boolean[]>([]);

const toggleMenu = (index: number) => {
  menuState.value = fields.value.map((_, i) => i === index ? !menuState.value[index] : false);
};

const editField = (index: number) => {
  console.log('Feld bearbeiten:', fields.value[index]);
};

// Löschbestätigung anzeigen
const confirmDelete = (index: number) => {
  selectedFieldIndex.value = index;
  showDeleteDialog.value = true;
};

// Feld löschen
const deleteField = async (index: number | null) => {
  if (index === null || index < 0 || index >= fields.value.length) {
    console.error('Ungültiger Index für das zu löschende Feld.');
    return;
  }

  const field = fields.value[index];
  if (!field) {
    console.error('Feld nicht gefunden.');
    return;
  }

  try {
    await api.delete(`/fields/delete/${field.id}/`);
    console.log(`Feld ${field.id} erfolgreich gelöscht`);
    fields.value.splice(index, 1); // Feld aus der Liste entfernen
    menuState.value.splice(index, 1); // Menüstatus ebenfalls aktualisieren
    showDeleteDialog.value = false;
  } catch (error) {
    console.error('Fehler beim Löschen des Feldes:', error);
  }
};


// Felder aus Backend laden
const fetchFields = async (): Promise<void> => {
  try {
    const response = await api.get('/fields/');
    fields.value = response.data;
    menuState.value = Array(fields.value.length).fill(false);
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error);
  }
};

const addField = async (fieldData: { width: number; height: number; saat_name: string }) => {
  try {
    const response = await api.post('/fields/add/', fieldData);
    fields.value.push(response.data);
    menuState.value.push(false);
    showAddFieldModal.value = false;
  } catch (error) {
    console.error('Fehler beim Hinzufügen eines neuen Feldes:', error);
  }
};

onMounted(fetchFields);
</script>
