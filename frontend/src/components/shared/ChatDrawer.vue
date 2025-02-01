<template>
  <div>
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

    <!-- Chat Drawer -->
    <q-drawer v-model="localChatDrawerOpen" side="right" :width="350" bordered class="drawer-style">
      <div class="q-pa-md drawer-header">
        <h5>{{ title }}</h5>
        <q-btn flat dense icon="close" class="float-right" @click="toggleChat" />
      </div>
      <q-separator />

      <!-- Chat-Verlauf -->
      <div class="q-pa-md chat-messages" ref="chatBox">
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
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch, nextTick } from 'vue';
import { api } from 'boot/axios';

const props = defineProps({
  chatDrawerOpen: Boolean,
  title: { type: String, default: 'Chat mit GPT' },
});

const emit = defineEmits(['update:chatDrawerOpen']);
const localChatDrawerOpen = ref(props.chatDrawerOpen);

watch(() => props.chatDrawerOpen, (newValue) => {
  localChatDrawerOpen.value = newValue;
});

const toggleChat = () => {
  localChatDrawerOpen.value = !localChatDrawerOpen.value;
  emit('update:chatDrawerOpen', localChatDrawerOpen.value);
};

const chatMessages = ref([{ role: 'gpt', text: 'Willkommen! Wie kann ich dir helfen?' }]);
const userMessage = ref('');
const chatBox = ref<HTMLElement | null>(null);

const sendMessage = async () => {
  if (!userMessage.value.trim()) return;

  chatMessages.value.push({ role: 'user', text: userMessage.value });
  const userInput = userMessage.value;
  userMessage.value = '';

  chatMessages.value.push({ role: 'gpt', text: 'GPT schreibt...' });
  await scrollToBottom();

  try {
    const response = await api.post('/chat/', { message: userInput, system_message: 'Bitte antworte immer auf Deutsch.' });
    chatMessages.value.pop();
    chatMessages.value.push({ role: 'gpt', text: response.data.reply });
    await scrollToBottom();
  } catch (error) {
    console.error('Fehler beim Abrufen der GPT-Antwort:', error);
    chatMessages.value.pop();
    chatMessages.value.push({ role: 'gpt', text: 'Entschuldigung, etwas ist schiefgelaufen.' });
    await scrollToBottom();
  }
};

const scrollToBottom = async () => {
  await nextTick();
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight;
};
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
  max-height: 70vh;
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

.chat-input {
  position: sticky;
  bottom: 0;
  padding: 16px;
  background: #fff;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

/* Floating Button */
.chat-fab {
  position: fixed;
  bottom: 80px;
  right: 16px;
  z-index: 10000;
}
</style>
