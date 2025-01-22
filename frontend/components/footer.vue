<template>
  <q-footer elevated class="bg-gray-800 text-white p-4">
    <div class="flex justify-between items-center">
      <span>&copy; 2025 Farmers Hub</span>
      <q-btn flat color="white" label="Impressum" @click="goToImpressum" />
      <q-btn flat color="white" label="Mehr über uns" @click="goToAbout" />
    </div>
  </q-footer>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goToAbout = () => {
  router.push("/about");
};

const goToImpressum = () => {
  router.push("/impressum");
};
</script>
