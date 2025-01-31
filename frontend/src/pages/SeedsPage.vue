<template>
  <q-page class="q-pa-md">
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Saatgutverwaltung</h3>
      </q-card-section>

      <!-- Tabelle mit Saatgut -->
      <q-card-section>
        <q-table
          flat
          bordered
          :rows="seeds"
          :columns="columns"
          row-key="id"
        >
          <template v-slot:body-cell-actions="props">
            <q-td :props="props">
              <q-btn
                flat
                icon="delete"
                color="red"
                @click="deleteSeed(props.row.id)"
              />
            </q-td>
          </template>
        </q-table>
      </q-card-section>

      <!-- Button zum Hinzufügen von Saatgut -->
      <q-card-actions align="right">
        <q-btn label="Neues Saatgut hinzufügen" color="primary" @click="openSeedDialog" />
      </q-card-actions>
    </q-card>

    <!-- Dialog zum Hinzufügen -->
    <q-dialog v-model="isSeedDialogOpen">
      <q-card>
        <q-card-section>
          <h3>Neues Saatgut registrieren</h3>
          <q-input v-model="newSeed.name" label="Saatgutname" />
          <q-input v-model="newSeed.mass_kg" label="Masse (kg)" type="number" />
          <q-input v-model="newSeed.pref_temperature" label="Bevorzugte Temperatur (°C)" type="number" />
          <q-input v-model="newSeed.pref_humidity" label="Bevorzugte Luftfeuchte (%)" type="number" />
          <q-input v-model="newSeed.pref_soil_moisture" label="Bevorzugte Bodenfeuchte (%)" type="number" />
          <q-input v-model="newSeed.pref_nutrient_level" label="Nährstofflevel" type="number" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn label="Abbrechen" flat @click="isSeedDialogOpen = false" />
          <q-btn label="Speichern" color="primary" @click="addSeed" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { api } from "boot/axios";

const seeds = ref([]);
const isSeedDialogOpen = ref(false);
const newSeed = ref({
  name: "",
  mass_kg: null,
  pref_temperature: null,
  pref_humidity: null,
  pref_soil_moisture: null,
  pref_nutrient_level: null,
});

// Spalten für die Tabelle
const columns = [
  { name: "name", label: "Saatgutname", align: "left" as const, field: "name" },
  { name: "mass_kg", label: "Masse (kg)", align: "left" as const, field: "mass_kg" },
  { name: "pref_temperature", label: "Temp. (°C)", align: "left" as const, field: "pref_temperature" },
  { name: "pref_humidity", label: "Feuchte (%)", align: "left" as const, field: "pref_humidity" },
  { name: "pref_soil_moisture", label: "Bodenfeuchte (%)", align: "left" as const, field: "pref_soil_moisture" },
  { name: "pref_nutrient_level", label: "Nährstoffe", align: "left" as const, field: "pref_nutrient_level" },
  { name: "actions", label: "Aktionen", align: "center" as const, field: "actions" },
];

// Saatgut abrufen
const fetchSeeds = async () => {
  try {
    const response = await api.get("/seeds/");
    seeds.value = response.data;
  } catch (error) {
    console.error("Fehler beim Abrufen der Saatgutsorten:", error);
  }
};

// Neues Saatgut hinzufügen
const openSeedDialog = () => {
  isSeedDialogOpen.value = true;
};

const addSeed = async () => {
  try {
    await api.post("/seeds/add/", newSeed.value);
    isSeedDialogOpen.value = false;
    await fetchSeeds(); // Liste aktualisieren
  } catch (error) {
    console.error("Fehler beim Hinzufügen des Saatguts:", error);
  }
};

// Saatgut löschen
const deleteSeed = async (seedId: number) => {
  try {
    await api.delete(`/seeds/delete/${seedId}/`);
    await fetchSeeds(); // Liste aktualisieren
  } catch (error) {
    console.error("Fehler beim Löschen des Saatguts:", error);
  }
};

onMounted(fetchSeeds);
</script>
