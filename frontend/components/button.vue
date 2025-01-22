<template>
  <q-btn
    :label="label"
    :color="color"
    class="q-px-md q-py-sm text-white q-font-medium"
    @click="onClick"
  />
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  color: { type: String, default: "primary" },
  onClick: { type: Function, required: false },
});
</script>
