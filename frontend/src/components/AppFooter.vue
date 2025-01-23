<template>
  <q-footer elevated class="bg-dark text-white q-pa-md">
    <div class="row justify-between items-center">
      <span>&copy; 2025 Farmers Hub</span>
      <q-btn flat color="white" label="Impressum" @click="goTo('/impressum')" />
      <q-btn flat color="white" label="Mehr über uns" @click="goTo('/about')" />
    </div>
  </q-footer>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";

const router = useRouter();

const goTo = (path: string): void => {
  void router.push(path);
};

</script>
