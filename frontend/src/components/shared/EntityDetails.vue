<template>
  <InfoCard :title="title">
    <p v-for="(value, key) in details" :key="key">
      <strong>{{ formatLabel(key) }}:</strong> {{ value || 'Nicht verfügbar' }}
    </p>
    <template v-slot:actions>
      <q-btn flat label="Zurück" color="primary" @click="$emit('goBack')" />
    </template>
  </InfoCard>
</template>

<script setup lang="ts">
import InfoCard from 'src/components/shared/InfoCard.vue';

defineProps({
  title: { type: String, required: true },
  details: { type: Object, required: true },
});

defineEmits(['goBack']);

const formatLabel = (key: string) => {
  const labels: { [key: string]: string } = {
    name: 'Name',
    size: 'Größe (ha)',
    saat__name: 'Saatgut',
    created_at: 'Erstellt am',
    health_score: 'Health Score',
  };
  return labels[key] || key;
};
</script>
