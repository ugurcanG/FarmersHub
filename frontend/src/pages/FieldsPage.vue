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
        <Card :title="'Feld ' + field.id" :content="'Größe: ' + field.size + ' ha'">
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
              <Button class="btn btn-flat text-dark rounded" color="white" @click="addField">
                <i class="material-icons text-h5 text-dark">add</i>
              </Button>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from 'boot/axios'; // Axios-Instanz
import Card from 'src/components/BaseCard.vue';
import Button from 'src/components/BaseButton.vue';

interface Field {
  id: number;
  size: number;
  created_at: string;
  saat_name: string | null;
}

const fields = ref<Field[]>([]);

// Felder aus Backend laden
const fetchFields = async (): Promise<void> => {
  try {
    const response = await api.get('/fields/');
    fields.value = response.data; // Daten setzen
  } catch (error) {
    console.error('Fehler beim Abrufen der Felder:', error);
  }
};

const addField = (): void => {
  console.log("Neue Felder hinzufügen ist noch nicht implementiert!");
};

const handleMoreVert = (index: number): void => {
  console.log(`Optionen für Feld mit Index ${index}`);
};

// Beim Laden der Seite Felder abrufen
onMounted(() => {
  fetchFields();
});
</script>
