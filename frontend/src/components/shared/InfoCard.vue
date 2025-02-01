<template>
  <q-card class="q-pa-md shadow-2">
    <q-card-section>
      <h3 class="text-h5 text-primary">{{ title }}</h3>
    </q-card-section>
    <q-card-section>
      <slot></slot> <!-- Hier kann beliebiger Inhalt rein -->
    </q-card-section>
    <q-card-actions align="right">
      <slot name="actions"></slot> <!-- Buttons oder weitere Slots -->
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
});
</script>
