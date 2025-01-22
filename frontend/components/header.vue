<template>
  <q-header elevated class="bg-blue-500 text-white">
    <q-toolbar>
      <q-btn flat dense round icon="menu" @click="toggleDrawer" />
      <q-toolbar-title>Farmers Hub</q-toolbar-title>
    </q-toolbar>
  </q-header>
</template>

<script setup>
const toggleDrawer = () => {
  console.log("Drawer geöffnet/geschlossen!");
};
</script>
