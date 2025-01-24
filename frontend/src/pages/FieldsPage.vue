<template>
  <q-page class="q-pa-md">
    <h3 class="text-h5 text-dark">Felder</h3>
    <div class="row q-col-gutter-lg">
      <!-- Bestehende Felder anzeigen -->
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
            <Button
              color="white"
              class="q-btn q-btn-item q-btn-round q-btn-flat"
              @click="handleMoreVert(index)"
            >
              <i class="material-icons text-dark">more_vert</i>
            </Button>
          </template>
          <template #image>
            <!-- Quadrat, das das Feld repräsentiert -->
            <div
              class="bg-green-5"
              style="width: 100px; height: 100px; transform: rotate(15deg);"
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

    <!-- Ausgelagertes Modal -->
    <FieldModal
      :showModal="showAddFieldModal"
      @close="showAddFieldModal = false"
      @submit="addField"
    />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios'; // Axios-Instanz
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

const handleMoreVert = (index: number) => {
  console.log('More options for field at index:', index);
};

// Felder aus Backend laden
const fetchFields = async (): Promise<void> => {
  try {
    const response = await api.get('/fields/');
    console.log('Felder abgerufen:', response.data);
    fields.value = response.data;
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error);
  }
};

// Neues Feld erstellen
const addField = async (fieldData: { width: number; height: number; saat_name: string }) => {
  try {
    const response = await api.post('/fields/add/', fieldData);
    console.log('Feld hinzugefügt:', response.data);
    fields.value.push(response.data); // Neues Feld zur Liste hinzufügen
    showAddFieldModal.value = false;
  } catch (error) {
    console.error('Fehler beim Hinzufügen eines neuen Feldes:', error);
  }
};

// Beim Laden der Seite Felder abrufen
onMounted(async () => {
  await fetchFields();
});
</script>

<style scoped>
.content-container {
  position: relative;
}
.saat-info {
  position: absolute;
  bottom: 0;
  right: 0;
  font-size: 0.9rem;
  color: white;
  margin: 0;
  padding: 0.5rem;
  border-radius: 4px;
}
</style>
