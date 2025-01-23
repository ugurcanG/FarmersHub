<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Navbar -->
    <Navbar />

    <!-- Left Drawer (optional) -->
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label header>
          Navigation
        </q-item-label>
        <q-item
          v-for="link in navigationLinks"
          :key="link.path"
          clickable
          @click="navigate(link.path)"
        >
          <q-item-section avatar>
            <q-icon :name="link.icon" />
          </q-item-section>
          <q-item-section>{{ link.label }}</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <!-- Main Page Content -->
    <q-page-container>
      <router-view />
    </q-page-container>

    <!-- Footer -->
    <Footer />
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "components/AppNavbar.vue";
import Footer from "components/AppFooter.vue";

interface NavigationLink {
  label: string;
  path: string;
  icon: string;
}

const router = useRouter();
const leftDrawerOpen = ref<boolean>(false);

const navigationLinks: NavigationLink[] = [
  { label: "Felder", path: "/fields", icon: "grass" },
  { label: "Mitarbeiter", path: "/employees", icon: "people" },
  { label: "Maschinen", path: "/machines", icon: "settings" },
  { label: "Markt", path: "/market", icon: "store" },
];

const navigate = (path: string): void => {
  leftDrawerOpen.value = false;
  void router.push(path);
};
</script>

<style lang="scss">
/* Optional: Stile für Navbar und Footer können hier hinzugefügt werden */
</style>
