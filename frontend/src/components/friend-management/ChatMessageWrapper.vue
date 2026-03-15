<template>
  <div class="chat-message" :class="{ 'is-mine': isMine }">
    <div class="message-bubble">
      <div class="message-content">{{ message.content }}</div>
      <div class="message-time">{{ formatTime(message.timestamp) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { ChatMessage } from '@/types/friendTypes'

interface Props {
  message: ChatMessage
  currentUserId?: string
}

const props = withDefaults(defineProps<Props>(), {
  currentUserId: 'me'
})

const isMine = computed(() => props.message.senderId === 'me' || props.message.senderId === props.currentUserId)

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${hours}:${minutes}`
}
</script>

<style scoped>
.chat-message {
  display: flex;
  margin-bottom: 12px;
  animation: message-in 0.3s ease;
}

@keyframes message-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-message.is-mine {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 16px;
  position: relative;
}

.chat-message:not(.is-mine) .message-bubble {
  background: #fff;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.chat-message.is-mine .message-bubble {
  background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 100%);
  color: #fff;
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(116, 148, 236, 0.3);
}

.message-content {
  font-size: 14px;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-time {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
  text-align: right;
}
</style>