<template>
  <q-page class="q-pa-md">
    <h1 class="text-h4 text-left">Dashboard</h1>
    <p class="text-body1">
      Willkommen beim Farmers Hub Dashboard! Hier findest du alle wichtigen Informationen auf einen Blick.
    </p>
    <div class="row q-col-gutter-lg">
      <div class="col-12 col-sm-6 col-md-4">
        <Card title="Felder" content="Verwalte und analysiere deine Felddaten.">
          <template #actions>
            <Button label="Details" icon="grass" color="green" :onClick="goToFields" />
          </template>
        </Card>
      </div>
      <div class="col-12 col-sm-6 col-md-4">
        <Card title="Mitarbeiter" content="Behalte den Überblick über deine Mitarbeiter.">
          <template #actions>
            <Button label="Details" icon="people" color="blue" :onClick="goToEmployees" />
          </template>
        </Card>
      </div>
      <div class="col-12 col-sm-6 col-md-4">
        <Card title="Maschinen" content="Überwache und plane deine Maschinenwartung.">
          <template #actions>
            <Button label="Details" icon="build" color="red" :onClick="goToMachines" />
          </template>
        </Card>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import Card from 'src/components/BaseCard.vue';
import Button from 'src/components/BaseButton.vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const goToFields = () => {
  void router.push('/fields');
};

const goToEmployees = () => {
  void router.push('/employees');
};

const goToMachines = () => {
  void router.push('/machines');
};
</script>
