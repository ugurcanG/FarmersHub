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
        <Card :title="field.name" :content="field.description">
          <template #icon>
            <Button
              color="white"
              class="q-btn q-btn-item q-btn-round q-btn-flat"
              @click="handleMoreVert(index)"
            >
              <i class="material-icons text-dark">more_vert</i>
            </Button>
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
                @click="addField"
              >
                <i class="material-icons text-h5 text-dark">add</i>
              </Button>
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
import Button from "@/components/button.vue";

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

const handleMoreVert = (index) => {
  console.log(`More options for field index ${index}`);
};
</script>
