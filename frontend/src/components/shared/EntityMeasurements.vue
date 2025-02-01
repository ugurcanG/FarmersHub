<template>
  <InfoCard :title="title">
    <DataTable :rows="measurements" :columns="columns" @refresh="fetchMeasurements" />
  </InfoCard>
</template>

<script setup lang="ts">
import InfoCard from 'src/components/shared/InfoCard.vue';
import DataTable from 'src/components/shared/DataTable.vue';
import type { PropType } from 'vue';

defineProps({
  title: { type: String, default: 'Messwerte' },
  measurements: { type: Array as PropType<Record<string, unknown>[]>, required: true },
  columns: { type: Array as PropType<Array<{
    name: string;
    label: string;
    field: string | ((row: Record<string, unknown>) => unknown);
    align?: "left" | "right" | "center";
    sortable?: boolean;
  }>>, required: true },
  fetchMeasurements: { type: Function as PropType<() => Promise<void>>, required: true },
});
</script>
