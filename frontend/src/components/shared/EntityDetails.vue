<template>
  <q-card class="q-pa-md shadow-2">
    <q-card-section>
      <h3 class="text-h5 text-primary">{{ title }}</h3>
    </q-card-section>
    <q-card-section>
      <div v-for="(value, key) in details" :key="key">
        <p><strong>{{ labels[key] || key }}:</strong> {{ formatValue(value, key) }}</p>
      </div>
    </q-card-section>
    <q-card-actions align="right">
      <slot name="actions"></slot>
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
  title: { type: String, required: true },
  details: { type: Object, required: true },
  labels: { type: Object, default: () => ({}) }, // Labels für Schlüssel der Details
  formatMap: { type: Object, default: () => ({}) } // Funktionen zur speziellen Formatierung
});

const formatValue = (value: unknown, key: string): string => {
  if (props.formatMap[key]) return props.formatMap[key](value);

  if (value === null || value === undefined) return 'Nicht verfügbar';

  if (typeof value === 'object') {
    if (Array.isArray(value)) return value.join(', ');
    return '[Objekt]';
  }

  return typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean'
    ? String(value)
    : 'Nicht verfügbar';
};
</script>
