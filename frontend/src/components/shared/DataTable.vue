<template>
  <q-table :rows="rows" :columns="columns" row-key="id" flat bordered>
    <template v-slot:top-right>
      <q-btn flat icon="refresh" @click="$emit('refresh')" label="Aktualisieren" />
    </template>
  </q-table>
</template>

<script setup lang="ts">
defineProps<{
  rows: readonly Record<string, unknown>[],
  columns: {
    name: string;
    label: string;
    field: string | ((row: Record<string, unknown>) => unknown);
    required?: boolean;
    align?: "left" | "right" | "center";
    sortable?: boolean;
    sort?: (a: unknown, b: unknown, rowA: Record<string, unknown>, rowB: Record<string, unknown>) => number;
    format?: (val: unknown, row: Record<string, unknown>) => unknown;
    style?: string | ((row: Record<string, unknown>) => string);
    classes?: string | ((row: Record<string, unknown>) => string);
    headerStyle?: string;
    headerClasses?: string;
  }[],
}>()
defineEmits(['refresh'])
</script>
