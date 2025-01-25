<template>
  <q-page class="q-pa-md">
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Details für Feld: {{ field.name }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Größe:</strong> {{ field.size }} ha</p>
        <p><strong>Saatgut:</strong> {{ field.saat__name || 'Kein Saatgut zugewiesen' }}</p>
        <p><strong>Erstellt am:</strong> {{ field.created_at }}</p>
        <p><strong>Health Score:</strong> {{ field.health_score }}</p>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from 'boot/axios';

const field = ref({
  id: 0,
  name: '',
  size: 0,
  created_at: '',
  saat__name: null,
  health_score: null,
});

const route = useRoute();
const router = useRouter();
const fieldId = String(route.params.id); // Sicherstellen, dass es eine Zeichenkette ist

const fetchFieldDetails = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/`);
    field.value = response.data;
  } catch (error) {
    console.error('Fehler beim Abrufen der Felddetails:', error);
    await router.push('/fields'); // Korrekte Verwendung von await
  }
};

const goBack = async () => {
  await router.push('/fields'); // Korrekte Verwendung von await
};

onMounted(fetchFieldDetails);
</script>
