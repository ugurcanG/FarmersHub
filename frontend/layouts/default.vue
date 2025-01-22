<template>
  <q-layout view="lHh Lpr lFf" class="bg-gray-100">
    <!-- Header -->
    <Header />
    <!-- Navbar -->
    <Navbar />

    <!-- Hauptinhalt -->
    <q-page-container>
      <slot />
    </q-page-container>

    <!-- Footer -->
    <Footer />
  </q-layout>
</template>

<script setup>
import Header from "@/components/header.vue";
import Footer from "@/components/footer.vue";
import navbar from "~/components/navbar.vue";
</script>
