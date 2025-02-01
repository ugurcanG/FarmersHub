<template>
  <q-table :rows="rows" :columns="columns" row-key="id" flat bordered>
    <template v-slot:top-right>
      <q-btn flat icon="refresh" @click="$emit('refresh')" label="Aktualisieren" />
    </template>
  </q-table>
</template>

<script setup lang="ts">
defineProps({
  rows: Array,
  columns: Array,
});
defineEmits(['refresh']);
</script>
