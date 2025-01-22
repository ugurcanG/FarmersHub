<template>
  <q-layout view="lHh Lpr lFf" class="bg-gray-100">
    <q-page-container>
      <div class="p-6 space-y-6">
        <h1 class="text-3xl font-bold text-center text-gray-800">Dashboard</h1>
        <p class="text-gray-600 text-lg">
          Willkommen beim Farmers Hub Dashboard! Hier findest du alle wichtigen Informationen auf einen Blick.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card
            title="Felder"
            content="Verwalte und analysiere deine Felddaten."
          >
            <template #actions>
              <Button label="Details" color="green" :onClick="goToFields"></Button>
            </template>
          </Card>
          <Card
            title="Mitarbeiter"
            content="Behalte den Überblick über deine Mitarbeiter."
          >
            <template #actions>
              <Button label="Details" color="blue" :onClick="goToEmployees"></Button>
            </template>
          </Card>
          <Card
            title="Maschinen"
            content="Überwache und plane deine Maschinenwartung."
          >
            <template #actions>
              <Button label="Details" color="red" :onClick="goToMachines"></Button>
            </template>
          </Card>
        </div>
      </div>
    </q-page-container>
    <Footer></Footer>
  </q-layout>
</template>

<script setup>
import Footer from '@/components/footer.vue';
import Card from '@/components/card.vue';
import Button from '@/components/button.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const goToFields = () => {
  router.push('/fields');
};

const goToEmployees = () => {
  router.push('/employees');
};

const goToMachines = () => {
  router.push('/machines');
};
</script>
