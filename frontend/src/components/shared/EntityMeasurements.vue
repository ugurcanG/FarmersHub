<template>
  <q-card class="q-pa-md shadow-2">
    <q-card-section>
      <h4 class="text-h6">{{ title }}</h4>
      <DataTable
        :rows="measurements"
        :columns="columns"
        @refresh="fetchMeasurements"
      />
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';
import DataTable from 'src/components/shared/DataTable.vue';

defineProps({
  title: { type: String, default: 'Messwerte' },
  measurements: { type: Array as PropType<Record<string, unknown>[]>, required: true },
  columns: { type: Array as PropType<Array<{
    name: string;
    label: string;
    field: string | ((row: Record<string, unknown>) => unknown);
    align?: 'left' | 'right' | 'center';
    sortable?: boolean;
  }>>, required: true },
  fetchMeasurements: { type: Function as PropType<() => Promise<void>>, required: true },
});
</script>
