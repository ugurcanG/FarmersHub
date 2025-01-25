<template>
  <q-page class="q-pa-md space-y-6">
    <h1 class="text-h5 text-center">Über Farmers Hub</h1>
    <p class="text-body1">
      Farmers Hub ist eine innovative Plattform, die Landwirte, Lohnunternehmer und
      landwirtschaftliche Dienstleister miteinander vernetzt.
    </p>
    <Card
      title="Unsere Mission"
      content="Die Effizienz steigern, Kosten senken und die Landwirtschaft revolutionieren."
    >
      <template #actions>
        <Button label="Mehr erfahren" color="primary" :onClick="goToDocumentation" />
      </template>
    </Card>
    <Card
      title="Unsere Vision"
      content="Ein digitales Ökosystem, das Tradition und Innovation vereint."
    >
      <template #actions>
        <Button label="Kontaktieren Sie uns" color="secondary" :onClick="contactUs" />
      </template>
    </Card>
  </q-page>
</template>

<script setup lang="ts">
import Card from 'src/components/BaseCard.vue'
import Button from 'src/components/BaseButton.vue'

const goToDocumentation = () => {
  console.log('Zur Dokumentation navigieren!')
}

const contactUs = () => {
  console.log('Kontaktformular öffnen!')
}
</script>
