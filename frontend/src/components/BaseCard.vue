<template>
  <q-card
    class="q-pa-md q-ma-sm shadow-2 column no-wrap relative-position card-equal-height"
    :style="{ backgroundColor }"
  >
    <!-- Titel und Icon -->
    <q-card-section class="row items-center justify-between q-gutter-sm">
      <div>
        <slot name="title">
          <h2 class="text-h6 text-white">{{ title }}</h2>
        </slot>
      </div>
      <div>
        <slot name="icon"></slot>
      </div>
    </q-card-section>

    <!-- Bildbereich -->
    <div class="flex flex-center q-mt-md q-mb-md">
      <slot name="image"></slot>
    </div>

    <!-- Inhalt -->
    <q-card-section class="text-body1 text-white">
      <slot name="content">{{ content }}</slot>
    </q-card-section>

    <!-- Aktionen -->
    <q-card-actions align="center">
      <slot name="actions"></slot>
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
defineProps({
  title: { type: String, default: '' },
  content: { type: String, default: '' },
  backgroundColor: { type: String, default: 'var(--q-primary)' },
})
</script>

<style lang="scss">
.card-equal-height {
  height: 300px; /* Gleiche Höhe für alle Karten */
}
</style>
