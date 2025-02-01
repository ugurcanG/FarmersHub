<template>
  <q-page class="q-pa-md" :class="{ 'page-with-drawer': chatDrawerOpen }">
    <!-- Basisdetails -->
    <q-card class="q-pa-md shadow-2">
      <q-card-section>
        <h3 class="text-h5 text-primary">Details für Feld: {{ field.name }}</h3>
      </q-card-section>
      <q-card-section>
        <p><strong>Größe:</strong> {{ field.size }} ha</p>
        <p><strong>Saatgut:</strong> {{ field.saat__name || 'Kein Saatgut zugewiesen' }}</p>
        <p><strong>Erstellt am:</strong> {{ field.created_at }}</p>
        <p><strong>Health Score:</strong> {{ field.health_score }}</p>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="Zurück" color="primary" @click="goBack" />
      </q-card-actions>
    </q-card>

    <!-- Tabelle der Messwerte -->
    <q-card class="q-pa-md shadow-2 q-mt-md">
      <q-card-section>
        <h4 class="text-h6">Messwerte</h4>
        <q-table :rows="fieldMeasurements" :columns="columns" row-key="id" flat bordered>
          <template v-slot:top-right>
            <q-btn flat icon="refresh" @click="fetchMeasurements" label="Aktualisieren" />
          </template>
        </q-table>
      </q-card-section>
    </q-card>
    <ChartContainer
  :labels="labels"
  :data="formattedData"
  :chartOptions="chartOptions"
  title="Messwerte-Analyse"
/>

    <!-- Floating Button -->
    <q-btn
      v-if="!chatDrawerOpen"
      round
      glossy
      icon="chat"
      color="primary"
      class="chat-fab"
      @click="toggleChat"
    />
  </q-page>
  <!-- Chat Drawer -->
  <q-drawer v-model="chatDrawerOpen" side="right" :width="350" bordered class="drawer-style">
    <!-- Chat Header -->
    <div class="q-pa-md drawer-header">
      <h5>Chat mit GPT</h5>
      <q-btn flat dense icon="close" class="float-right" @click="toggleChat" />
    </div>
    <q-separator />

    <!-- Chat-Verlauf -->
    <div class="q-pa-md chat-messages">
      <div v-for="(msg, index) in chatMessages" :key="index" class="chat-message">
        <div :class="['message', msg.role === 'gpt' ? 'left' : 'right']">
          <p>{{ msg.text }}</p>
        </div>
      </div>
    </div>

    <!-- Eingabezeile -->
    <q-separator />
    <div class="q-pa-md chat-input">
      <q-input
        v-model="userMessage"
        placeholder="Nachricht eingeben..."
        dense
        outlined
        @keyup.enter="sendMessage"
      >
        <template v-slot:append>
          <q-btn flat icon="send" color="primary" @click="sendMessage" />
        </template>
      </q-input>
    </div>
  </q-drawer>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onBeforeUnmount, defineProps } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'boot/axios'
import type { FieldMeasurement } from 'src/components/models';
import ChartContainer from 'src/components/shared/ChartContainer.vue'


defineProps({
  id: {
    type: String,
    required: false, // Falls `id` nicht zwingend erforderlich ist
  },
})
// Floating Button und Drawer-Status
const chatDrawerOpen = ref(false)

// Chat-Verlauf und Eingabe
const chatMessages = ref([{ role: 'gpt', text: 'Willkommen! Wie kann ich dir helfen?' }])
const userMessage = ref('')

// Toggle für den Chat Drawer
const toggleChat = () => {
  chatDrawerOpen.value = !chatDrawerOpen.value
}

// Nachricht senden
const sendMessage = async () => {
  if (!userMessage.value.trim()) return

  // Nachricht des Benutzers hinzufügen
  chatMessages.value.push({ role: 'user', text: userMessage.value })

  const userInput = userMessage.value
  userMessage.value = '' // Eingabefeld leeren

  // "GPT schreibt..." Nachricht hinzufügen
  const typingIndicator = { role: 'gpt', text: 'GPT schreibt...' }
  chatMessages.value.push(typingIndicator)
  scrollToBottom()

  try {
    // Anfrage an Backend senden
    const response = await api.post('/chat/', {
      message: userInput,
      system_message: 'Bitte antworte immer auf Deutsch.',
    })

    // GPT-Antwort hinzufügen
    const gptReply = response.data.reply
    chatMessages.value.pop() // Entferne "GPT schreibt..." Nachricht
    chatMessages.value.push({ role: 'gpt', text: gptReply })
    scrollToBottom()
  } catch (error) {
    console.error('Fehler beim Abrufen der GPT-Antwort:', error)
    // "GPT schreibt..." Nachricht entfernen
    chatMessages.value.pop()
    chatMessages.value.push({ role: 'gpt', text: 'Entschuldigung, etwas ist schiefgelaufen.' })
    scrollToBottom()
  }
}

// Automatisches Scrollen zum letzten Chat
const scrollToBottom = () => {
  const chatBox = document.querySelector('.chat-messages')
  if (chatBox) chatBox.scrollTop = chatBox.scrollHeight
}

const field = ref({
  id: 0,
  name: '',
  size: 0,
  created_at: '',
  saat__name: null,
  health_score: null,
})

const fieldMeasurements = ref<FieldMeasurement[]>([])
const columns = [
  {
    name: 'created_at',
    label: 'Datum',
    align: 'left' as const,
    field: 'created_at',
    sortable: true,
  },
  {
    name: 'temperature',
    label: 'Temperatur (°C)',
    align: 'right' as const,
    field: 'temperature',
    sortable: true,
  },
  {
    name: 'humidity',
    label: 'Luftfeuchtigkeit (%)',
    align: 'right' as const,
    field: 'humidity',
    sortable: true,
  },
  {
    name: 'soil_moisture',
    label: 'Bodenfeuchte (%)',
    align: 'right' as const,
    field: 'soil_moisture',
    sortable: true,
  },
  {
    name: 'nutrients_level',
    label: 'Nährstoffe',
    align: 'right' as const,
    field: 'nutrients_level',
    sortable: true,
  },
  {
    name: 'health_score',
    label: 'Health Score',
    align: 'right' as const,
    field: 'health_score',
    sortable: true,
  },
]

const route = useRoute()
const router = useRouter()
const fieldId = String(route.params.id)

const fetchFieldDetails = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/`)
    field.value = response.data
  } catch (error) {
    console.error('Fehler beim Abrufen der Felddetails:', error)
    await router.push('/fields')
  }
}

const fetchMeasurements = async () => {
  try {
    const response = await api.get(`/fields/${fieldId}/measurements/`)
    fieldMeasurements.value = response.data
    console.log('Fetched Measurements:', fieldMeasurements.value) // Log die rohen Messwerte
  } catch (error) {
    console.error('Fehler beim Abrufen der Messwerte:', error)
  }
}

const labels = ref<string[]>([]);
const formattedData = ref<{ [key: string]: number }[]>([]);
const chartOptions = ref([
  { label: 'Temperatur (°C)', value: 'temperature' },
  { label: 'Luftfeuchtigkeit (%)', value: 'humidity' },
  { label: 'Bodenfeuchte (%)', value: 'soil_moisture' },
  { label: 'Nährstoffe', value: 'nutrients_level' },
  { label: 'Health Score', value: 'health_score' },
]);

watch(fieldMeasurements, () => {
  labels.value = fieldMeasurements.value.map((m) =>
    new Date(m.created_at).toLocaleDateString()
  );

  formattedData.value = fieldMeasurements.value.map((m) => ({
    temperature: m.temperature || 0,
    humidity: m.humidity || 0,
    soil_moisture: m.soil_moisture || 0,
    nutrients_level: m.nutrients_level || 0,
    health_score: m.health_score || 0,
  }));
});

const goBack = async () => {
  await router.push('/fields')
}

// Initialisierung
onMounted(async () => {
  await fetchFieldDetails()
  await fetchMeasurements()
})
</script>

<style>
.q-page {
  position: relative;
  overflow-x: hidden; /* Keine horizontale Überlappung zulassen */
}
.q-pa-md {
  transition: margin-right 0.3s ease;
  overflow: hidden; /* Verhindert, dass Inhalte über den Rand hinausgehen */
}
/* Floating Button */
.chat-fab {
  position: fixed;
  bottom: 80px;
  right: 16px;
  z-index: 10000;
}

.chat-input {
  position: sticky; /* Behält die Position relativ zum Drawer */
  bottom: 0; /* Am unteren Rand */
  padding: 16px;
  background: #fff; /* Hintergrundfarbe, um Nachrichten zu überdecken */
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); /* Leichter Schatten für Trennung */
  z-index: 1; /* Sicherstellen, dass es über den Nachrichten bleibt */
}

.page-with-drawer {
  transition: margin-right 0.3s ease;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
