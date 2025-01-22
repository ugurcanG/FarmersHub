<template>
  <q-layout view="lHh Lpr lFf">
    <Navbar />
    <q-page-container>
      <slot></slot>
    </q-page-container>
    <Footer />
  </q-layout>
</template>

<script setup>
import Navbar from '@/components/navbar.vue';
import Footer from '@/components/footer.vue';
</script>
