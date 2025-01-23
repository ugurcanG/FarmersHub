<template>
  <q-header elevated class="bg-primary text-white">
    <q-toolbar>
      <q-toolbar-title class="q-font-bold cursor-pointer" @click="goTo('/')">
        Farmers Hub
      </q-toolbar-title>
      <q-btn-group flat>
        <q-btn
          v-for="link in links"
          :key="link.path"
          :label="link.label"
          :flat="true"
          :class="{'text-secondary': isActive(link.path)}"
          @click="goTo(link.path)"
        />
      </q-btn-group>
    </q-toolbar>
  </q-header>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

interface Link {
  label: string;
  path: string;
}

const links: Link[] = [
  { label: "Felder", path: "/fields" },
  { label: "Mitarbeiter", path: "/employees" },
  { label: "Maschinen", path: "/machines" },
  { label: "Markt", path: "/market" },
];

const goTo = (path: string): void => {
  void router.push(path);
};

const isActive = (path: string): boolean => route.path === path;
</script>
