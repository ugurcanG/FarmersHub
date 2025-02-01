<template>
  <q-drawer v-model="chatDrawerOpen" side="right" :width="350" bordered class="drawer-style">
    <div class="q-pa-md drawer-header">
      <h5>{{ title }}</h5>
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

    <q-separator />
    <!-- Eingabezeile -->
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
import { ref, defineProps, defineEmits, watch, onMounted, nextTick } from 'vue'
import { api } from 'boot/axios'

const props = defineProps({
  chatDrawerOpen: Boolean,
  title: { type: String, default: 'Chat' },
})

const emit = defineEmits(['update:chatDrawerOpen'])
const chatMessages = ref([{ role: 'gpt', text: 'Willkommen! Wie kann ich dir helfen?' }])
const userMessage = ref('')

// Chat Drawer öffnen/schließen
const toggleChat = () => {
  emit('update:chatDrawerOpen', !props.chatDrawerOpen)
}

// Nachricht senden
const sendMessage = async () => {
  if (!userMessage.value.trim()) return

  // Nachricht des Benutzers hinzufügen
  chatMessages.value.push({ role: 'user', text: userMessage.value })

  const userInput = userMessage.value
  userMessage.value = '' // Eingabefeld leeren

  // "GPT schreibt..." Nachricht hinzufügen
  chatMessages.value.push({ role: 'gpt', text: 'GPT schreibt...' })
  scrollToBottom()

  try {
    // Anfrage an Backend senden
    const response = await api.post('/chat/', {
      message: userInput,
      system_message: 'Bitte antworte immer auf Deutsch.',
    })

    // GPT-Antwort hinzufügen
    chatMessages.value.pop() // Entferne "GPT schreibt..." Nachricht
    chatMessages.value.push({ role: 'gpt', text: response.data.reply })
    scrollToBottom()
  } catch (error) {
    console.error('Fehler beim Abrufen der GPT-Antwort:', error)
    chatMessages.value.pop()
    chatMessages.value.push({ role: 'gpt', text: 'Entschuldigung, etwas ist schiefgelaufen.' })
    scrollToBottom()
  }
}

// Automatisches Scrollen zum letzten Chat
const scrollToBottom = async () => {
  await nextTick()
  const chatBox = document.querySelector('.chat-messages')
  if (chatBox) chatBox.scrollTop = chatBox.scrollHeight
}
</script>

<style scoped>
.drawer-style {
  position: fixed;
  top: 0;
  right: 0;
  height: 100vh;
  width: 350px;
  background-color: #fff;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  z-index: 1100;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 75%;
  word-wrap: break-word;
}

.message.left {
  background-color: #f1f1f1;
  align-self: flex-start;
}

.message.right {
  background-color: #e0f7fa;
  align-self: flex-end;
  margin-left: auto;
}
</style>
