<template>
  <q-card class="shadow-md">
    <q-card-section>
      <slot name="title">
        <h2 class="text-xl font-bold">{{ title }}</h2>
      </slot>
    </q-card-section>
    <q-card-section>
      <slot name="content">
        <p>{{ content }}</p>
      </slot>
    </q-card-section>
    <q-card-actions align="right">
      <slot name="actions">
        <q-btn flat label="Schließen" color="primary" />
      </slot>
    </q-card-actions>
  </q-card>
</template>

<script setup>
defineProps({
  title: String,
  content: String,
});
</script>
