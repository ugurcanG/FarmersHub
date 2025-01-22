<template>
  <div class="q-pa-md">
    <h3 class="text-h5 text-dark">Felder</h3>
    <div class="row q-col-gutter-lg">
      <!-- Bestehende Felder anzeigen -->
      <div
        class="col-12 col-sm-6 col-md-4"
        v-for="(field, index) in fields"
        :key="index"
      >
        <Card
          :title="field.name"
          :content="field.description"
        />
      </div>
      
      <!-- Card für Hinzufügen -->
      <div class="col-12 col-sm-6 col-md-4">
        <Card>
          <template #content>
            <div class="q-pa-md flex flex-center text-center full-height">
              <button
                class="btn btn-flat text-dark rounded"
                @click="addField"
              >
                <i class="material-icons text-h5">add</i>
              </button>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Card from "@/components/card.vue";

const fields = ref([
  { name: "Feld 1", description: "Dies ist das erste Feld" },
  { name: "Feld 2", description: "Dies ist das zweite Feld" },
  { name: "Feld 3", description: "Dies ist das dritte Feld" },
]);

const addField = () => {
  const newFieldIndex = fields.value.length + 1;
  fields.value.push({
    name: `Feld ${newFieldIndex}`,
    description: `Dies ist das Feld Nummer ${newFieldIndex}`,
  });
};
</script>
