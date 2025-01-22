<template>
  <div>
    <!-- Barrierefreiheit unterstützen -->
    <NuxtRouteAnnouncer />

    <!-- Quasar-Layout -->
    <q-layout view="lHh Lpr lFf" class="bg-gray-100">
      <q-header elevated class="bg-blue-500 text-white">
        <q-toolbar>
          <q-toolbar-title>Nuxt + Quasar + Tailwind</q-toolbar-title>
        </q-toolbar>
      </q-header>
      <q-page-container>
        <!-- Seiteninhalt -->
        <NuxtPage />
      </q-page-container>
    </q-layout>
  </div>
</template>

<script setup>
import "quasar/dist/quasar.sass";
import "@quasar/extras/material-icons/material-icons.css";
</script>
