<template>
  <q-card
    class="q-pa-md q-ma-sm bg-primary text-white shadow-2 full-height column no-wrap relative-position"
  >
    <!-- Flexbox-Wrapper für Titel und Icon -->
    <q-card-section class="row items-center justify-between q-gutter-sm">
      <!-- Titel oben links -->
      <div>
        <slot name="title">
          <h2 class="text-h6">{{ title }}</h2>
        </slot>
      </div>

      <!-- Icon oben rechts -->
      <div>
        <slot name="icon"></slot>
      </div>
    </q-card-section>

    <!-- Inhalt -->
    <q-card-section class="text-body1">
      <slot name="content">
        <p>{{ content }}</p>
      </slot>
    </q-card-section>

    <!-- Actions -->
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
