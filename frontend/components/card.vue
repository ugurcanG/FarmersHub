<template>
  <q-card class="q-pa-md q-ma-sm bg-primary text-white shadow-2 full-height">
    <q-card-section>
      <slot name="title">
        <h2 class="text-h6">{{ title }}</h2>
      </slot>
    </q-card-section>
    <q-card-section class="text-body1">
      <slot name="content">
        <p>{{ content }}</p>
      </slot>
    </q-card-section>
    <q-card-actions align="center">
      <slot name="actions"></slot>
    </q-card-actions>
  </q-card>
</template>

<script setup>
defineProps({
  title: String,
  content: String,
});
</script>
