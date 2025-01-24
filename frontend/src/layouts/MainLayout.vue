<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Navbar -->
    <Navbar />

    <!-- Main Page Content -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <Footer />
  </q-layout>
</template>

<script setup lang="ts">
import Navbar from "components/AppNavbar.vue";
import Footer from "components/AppFooter.vue";
</script>

<style lang="scss">
/* Optional: Stile für Navbar und Footer können hier hinzugefügt werden */
</style>
