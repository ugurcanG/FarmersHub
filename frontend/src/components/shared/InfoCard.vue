<template>
  <q-card class="q-pa-md shadow-2">
    <q-card-section>
      <h4 class="text-h6">{{ title }}</h4>
      <slot></slot>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, required: true },
});
</script>
