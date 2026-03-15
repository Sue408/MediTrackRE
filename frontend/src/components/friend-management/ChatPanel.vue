<template>
  <div class="chat-panel">
    <!-- 空状态：未选择好友 -->
    <div class="empty-state" v-if="!selectedFriend">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z" fill="currentColor" opacity="0.2"/>
        <path d="M7 9h10v2H7zm0-3h10v2H7z" fill="currentColor" opacity="0.2"/>
      </svg>
      <p>选择一个好友开始聊天</p>
      <span>点击左侧好友列表中的好友</span>
    </div>

    <!-- 聊天界面 -->
    <template v-else>
      <!-- 聊天头部 -->
      <div class="chat-header">
        <div class="friend-info">
          <div class="avatar">
            {{ displayName.charAt(0).toUpperCase() }}
          </div>
          <div class="info">
            <div class="name">{{ displayName }}</div>
            <div class="status">{{ selectedFriend.status === 'online' ? '在线' : '离线' }}</div>
          </div>
        </div>
      </div>

      <!-- 消息列表 -->
      <div class="messages-container" ref="messagesContainer">
        <div class="messages-list">
          <ChatMessageWrapper
            v-for="message in messages"
            :key="message.id"
            :message="message"
          />
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="input-area">
        <input
          v-model="inputMessage"
          type="text"
          placeholder="输入消息..."
          @keyup.enter="handleSend"
          :disabled="sending"
        />
        <button class="send-btn" @click="handleSend" :disabled="!inputMessage.trim() || sending">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="currentColor"/>
          </svg>
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import type { Friend, ChatMessage } from '@/types/friendTypes'
import ChatMessageWrapper from './ChatMessageWrapper.vue'

interface Props {
  selectedFriend?: Friend
  messages: ChatMessage[]
  sending?: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  send: [content: string]
}>()

const inputMessage = ref('')
const messagesContainer = ref<HTMLElement>()

const displayName = computed(() => props.selectedFriend?.nickname || props.selectedFriend?.email.split('@')[0] || '')

const handleSend = () => {
  const content = inputMessage.value.trim()
  if (!content) return

  emit('send', content)
  inputMessage.value = ''
}

// 自动滚动到底部
watch(() => props.messages.length, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
})
</script>

<style scoped>
.chat-panel {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
  text-align: center;
  background: #fafafa;
}

.empty-state svg {
  margin-bottom: 20px;
  opacity: 0.4;
}

.empty-state p {
  margin: 0;
  font-size: 16px;
  color: #666;
}

.empty-state span {
  font-size: 13px;
  color: #999;
  margin-top: 8px;
}

.chat-header {
  padding: 16px 20px;
  background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 100%);
  color: #fff;
}

.friend-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.info .name {
  font-size: 16px;
  font-weight: 600;
}

.info .status {
  font-size: 12px;
  opacity: 0.8;
  margin-top: 2px;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fc;
}

.messages-list {
  display: flex;
  flex-direction: column;
}

.input-area {
  padding: 16px 20px;
  background: #fff;
  border-top: 1px solid #eee;
  display: flex;
  gap: 12px;
  align-items: center;
}

.input-area input {
  flex: 1;
  height: 42px;
  padding: 0 16px;
  border: 1px solid #e8e8e8;
  border-radius: 21px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
}

.input-area input:focus {
  border-color: #7494ec;
}

.input-area input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.send-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 100%);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(116, 148, 236, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>