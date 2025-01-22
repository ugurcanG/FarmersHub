<template>
  <q-header elevated class="bg-blue-600 text-white">
    <q-toolbar>
      <q-toolbar-title
        class="font-bold cursor-pointer hover:text-gray-300"
        @click="goToHomePage"
      >
        Farmers Hub
      </q-toolbar-title>
      <div class="flex space-x-4">
        <q-btn
          v-for="link in links"
          :key="link.path"
          flat
          :label="link.label"
          class="text-white"
          :class="{ 'text-gray-300': router.currentRoute.path === link.path }"
          @click="navigate(link.path)"
        />
      </div>
    </q-toolbar>
  </q-header>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

// Navigationslinks
const links = [
  { label: "Übersicht", path: "/dashboard" },
  { label: "Felder", path: "/fields" },
  { label: "Mitarbeiter", path: "/employees" },
  { label: "Maschinen", path: "/machines" },
  { label: "Markt", path: "/market" },
];

// Navigationsmethode
const navigate = (path) => {
  router.push(path);
};

const goToHomePage = () => {
  router.push("/");
};
</script>
