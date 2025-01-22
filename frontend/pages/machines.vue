<template>
  <q-layout view="lHh Lpr lFf" class="bg-gray-100">
    <q-page-container>
      <div class="p-6 space-y-6">
        <h1 class="text-2xl font-bold text-center text-gray-800">
          Maschinenmanagement
        </h1>
        <p class="text-gray-600 text-lg">
          Verwalten Sie Ihre Maschinen effizient und halten Sie den Betrieb
          aufrecht.
        </p>
        <Card
          v-for="machine in machines"
          :key="machine.id"
          :title="machine.name"
          :content="machine.status"
        >
          <template #actions>
            <Button
              label="Details anzeigen"
              color="blue"
              :onClick="() => viewDetails(machine.id)"
            ></Button>
          </template>
        </Card>
      </div>
    </q-page-container>
    <Footer></Footer>
  </q-layout>
</template>

<script setup>
import Footer from "@/components/footer.vue";
import Card from "@/components/card.vue";
import Button from "@/components/button.vue";

const machines = [
  { id: 1, name: "Traktor A", status: "In Betrieb" },
  { id: 2, name: "Mähdrescher B", status: "Wartung erforderlich" },
];

const viewDetails = (id) => {
  console.log("Maschinendetails anzeigen:", id);
};
</script>
