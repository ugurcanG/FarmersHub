<template>
  <q-btn
    :label="label"
    :color="color"
    class="rounded-md px-4 py-2 text-white font-semibold"
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
