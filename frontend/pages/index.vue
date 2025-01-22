<template>
  <q-layout view="lHh Lpr lFf" class="bg-gray-100">
    <q-header elevated class="bg-blue-500 text-white">
      <q-toolbar>
        <q-toolbar-title>Nuxt + Quasar + Tailwind</q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <div class="p-4">
        <!-- Button mit Klick-Handler -->
        <q-btn
          label="Primary Button"
          color="primary"
          class="px-6 py-3 text-lg font-bold"
          @click="showNotification"
        />
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { Notify } from "quasar"; // Notify-Plugin importieren
import "quasar/dist/quasar.sass";
import "@quasar/extras/material-icons/material-icons.css";

// Funktion für Notify
const showNotification = () => {
  Notify.create({
    message: "Das ist eine Testbenachrichtigung!",
    color: "green",
    position: "bottom-right",
  });
};
</script>
