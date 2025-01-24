<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4>Neues Feld erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="fieldData.width"
          type="number"
          label="Breite (ha)"
          filled
        />
        <q-input
          v-model="fieldData.height"
          type="number"
          label="Höhe (ha)"
          filled
        />
        <q-input
          v-model="fieldData.saat_name"
          label="Saatgut (optional)"
          filled
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn flat label="Abbrechen" @click="cancel" />
        <q-btn color="primary" label="Erstellen" @click="submitField" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, computed } from 'vue';

const emit = defineEmits(['close', 'submit']); // Emit-Events für den Parent
const { showModal } = defineProps({
  showModal: Boolean, // Erwartet Prop vom Parent
});

// Lokales `ref` für das Modal, synchronisiert mit `showModal`
const localShowModal = computed({
  get: () => showModal,
  set: (value) => {
    if (!value) emit('close'); // Schließt das Modal, wenn es deaktiviert wird
  },
});

const fieldData = ref({
  width: null as number | null,
  height: null as number | null,
  saat_name: '' as string,
});

const submitField = () => {
  if (!fieldData.value.width || !fieldData.value.height) {
    console.error('Breite und Höhe sind erforderlich!');
    return;
  }
  emit('submit', { ...fieldData.value }); // Daten an den Parent zurückgeben
  fieldData.value = { width: null, height: null, saat_name: '' }; // Eingabefelder zurücksetzen
};

const cancel = () => {
  emit('close'); // Modal schließen
};
</script>
