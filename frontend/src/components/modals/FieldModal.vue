<template>
  <q-dialog v-model="localShowModal">
    <q-card>
      <q-card-section>
        <h4 v-if="fieldToEdit">Feld bearbeiten</h4>
        <h4 v-else>Neues Feld erstellen</h4>
      </q-card-section>

      <q-card-section>
        <q-input
          v-model="fieldData.name"
          label="Name"
          filled
        />
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
        <q-btn
          color="primary"
          :label="fieldToEdit ? 'Speichern' : 'Erstellen'"
          @click="submitField"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, defineEmits, defineProps, computed, watch } from 'vue';
import type { PropType } from 'vue';

const emit = defineEmits(['close', 'submit']);
const { showModal, fieldToEdit } = defineProps({
  showModal: Boolean,
  fieldToEdit: {
    type: Object as PropType<{ width: number; height: number; saat_name: string } | null>,
    default: null,
  },
});

const localShowModal = computed({
  get: () => showModal,
  set: (value) => {
    if (!value) emit('close');
  },
});

// Typ für die Felddaten
interface FieldData {
  name: string,
  width: number | null;
  height: number | null;
  saat_name: string;
}

const fieldData = ref<FieldData>({
  name: '' as string,
  width: null,
  height: null,
  saat_name: '',
});

// Aktualisiere die Felddaten, wenn `fieldToEdit` sich ändert
watch(
  () => fieldToEdit,
  (newField) => {
    if (newField) {
      fieldData.value = { name: '', ...newField }; // Kopiere die Felddaten und füge den Namen hinzu
    } else {
      fieldData.value = { name: '',width: null, height: null, saat_name: '' }; // Zurücksetzen
    }
  },
  { immediate: true } // Direkt beim ersten Mounting ausführen
);

const submitField = () => {
  if (!fieldData.value.width || !fieldData.value.height) {
    console.error('Breite und Höhe sind erforderlich!');
    return;
  }
  emit('submit', { ...fieldData.value }); // Sende die Daten an den Parent
};

const cancel = () => {
  emit('close'); // Schließe das Modal
};
</script>
