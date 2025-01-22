import { defineNuxtConfig } from "nuxt/config";
import { quasar } from "@quasar/vite-plugin";
import path from "path";

export default defineNuxtConfig({
  compatibilityDate: "2025-01-22",
  devtools: { enabled: true },
  ssr: false,

  plugins: ["~/plugins/quasar.ts"],

  build: {
    transpile: ["quasar"],
  },

  vite: {
    plugins: [
      quasar({
        sassVariables: path.resolve(
          __dirname,
          "./assets/sass/quasar-variables.sass",
        ),
      }),
    ],
  },

  css: [
    "quasar/dist/quasar.sass",
  ],
});
