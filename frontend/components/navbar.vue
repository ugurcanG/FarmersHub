<template>
  <q-header elevated class="bg-primary text-white">
    <q-toolbar>
      <q-toolbar-title class="q-font-bold cursor-pointer" @click="goToHomePage">
        Farmers Hub
      </q-toolbar-title>
      <q-btn-group flat>
        <q-btn
          v-for="link in links"
          :key="link.path"
          :label="link.label"
          class="text-white"
          :class="{ 'text-secondary': router.currentRoute.path === link.path }"
          @click="navigate(link.path)"
        />
      </q-btn-group>
    </q-toolbar>
  </q-header>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const links = [
  { label: "Felder", path: "/fields" },
  { label: "Mitarbeiter", path: "/employees" },
  { label: "Maschinen", path: "/machines" },
  { label: "Markt", path: "/market" },
];

const navigate = (path) => {
  router.push(path);
};

const goToHomePage = () => {
  router.push("/");
};
</script>
