<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-center text-gray-800">
      Über Farmers Hub
    </h1>
    <p class="text-gray-600 text-lg">
      Farmers Hub ist eine innovative Plattform, die Landwirte, Lohnunternehmer
      und landwirtschaftliche Dienstleister miteinander vernetzt.
    </p>
    <Card
      title="Unsere Mission"
      content="Die Effizienz steigern, Kosten senken und die Landwirtschaft revolutionieren."
    >
      <template #actions>
        <Button
          label="Mehr erfahren"
          color="blue"
          :onClick="goToDocumentation"
        />
      </template>
    </Card>
    <Card
      title="Unsere Vision"
      content="Ein digitales Ökosystem, das Tradition und Innovation vereint."
    >
      <template #actions>
        <Button
          label="Kontaktieren Sie uns"
          color="green"
          :onClick="contactUs"
        />
      </template>
    </Card>
  </div>
</template>

<script setup>
import Card from "@/components/card.vue";
import Button from "@/components/button.vue";

const goToDocumentation = () => {
  console.log("Zur Dokumentation navigieren!");
};

const contactUs = () => {
  console.log("Kontaktformular öffnen!");
};
</script>
