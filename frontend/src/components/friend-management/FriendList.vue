<template>
  <div class="friend-list">
    <div class="list-header">
      <h4>好友列表</h4>
      <button class="add-btn" @click="handleAddFriend" title="添加好友">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z" fill="currentColor"/>
        </svg>
      </button>
    </div>

    <div class="list-content" v-if="friends.length > 0">
      <FriendItem
        v-for="friend in friends"
        :key="friend.id"
        :friend="friend"
        :is-active="selectedFriendId === friend.id"
        @click="handleSelectFriend"
        @contextmenu="handleContextMenu"
      />
    </div>

    <div class="empty-state" v-else>
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5s-3 1.34-3 3 1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z" fill="currentColor" opacity="0.3"/>
      </svg>
      <p>暂无好友</p>
      <span>点击上方 + 按钮添加好友</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Friend } from '@/types/friendTypes'
import FriendItem from './FriendItem.vue'

interface Props {
  friends: Friend[]
  selectedFriendId?: string
}

defineProps<Props>()

const emit = defineEmits<{
  select: [friend: Friend]
  contextmenu: [friend: Friend, event: MouseEvent]
  addfriend: []
}>()

const handleSelectFriend = (friend: Friend) => {
  emit('select', friend)
}

const handleContextMenu = (friend: Friend, event: MouseEvent) => {
  emit('contextmenu', friend, event)
}

const handleAddFriend = () => {
  emit('addfriend')
}
</script>

<style scoped>
.friend-list {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 5px 15px 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 10px;
}

.list-header h4 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.5px;
}

.add-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.add-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: scale(1.1);
}

.list-content {
  flex: 1;
  overflow-y: auto;
  padding-right: 5px;
}

.list-content::-webkit-scrollbar {
  width: 4px;
}

.list-content::-webkit-scrollbar-track {
  background: transparent;
}

.list-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
}

.empty-state svg {
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-state p {
  margin: 0;
  font-size: 15px;
  color: rgba(255, 255, 255, 0.7);
}

.empty-state span {
  font-size: 12px;
  margin-top: 5px;
  opacity: 0.6;
}
</style>