<template>
  <q-btn
    :label="label"
    :color="color"
    class="q-px-md q-py-sm text-white q-font-medium"
    @click="onClick"
    v-bind="props"
  >
    <slot />
  </q-btn>
</template>

<script setup>
defineProps({
  label: { type: String, default: "" },
  color: { type: String, default: "primary" },
  onClick: { type: Function, required: false },
  props: { type: Object, default: () => ({}) },
});
</script>
