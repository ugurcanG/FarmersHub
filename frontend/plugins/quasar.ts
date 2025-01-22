import { defineNuxtPlugin } from "#app";
import { Quasar, Notify } from "quasar";

export default defineNuxtPlugin((nuxtApp) => {
  if (import.meta.client) {
    // Sicherstellen, dass Quasar nur im Browser läuft
    nuxtApp.vueApp.use(Quasar, {
      plugins: { Notify },
    });
  }
});
