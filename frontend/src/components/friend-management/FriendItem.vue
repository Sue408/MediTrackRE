<template>
  <div
    class="friend-item"
    :class="{ active: isActive }"
    @click="handleClick"
    @contextmenu.prevent="handleContextMenu"
  >
    <div class="avatar-wrapper">
      <div class="avatar">
        {{ displayName.charAt(0).toUpperCase() }}
      </div>
      <span class="status-dot" :class="friend.status"></span>
    </div>
    <div class="info">
      <div class="nickname">{{ displayName }}</div>
      <div class="email">{{ friend.email }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Friend } from '@/types/friendTypes'

interface Props {
  friend: Friend
  isActive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isActive: false
})

const emit = defineEmits<{
  click: [friend: Friend]
  contextmenu: [friend: Friend, event: MouseEvent]
}>()

const displayName = computed(() => props.friend.nickname || props.friend.email.split('@')[0])

const handleClick = () => {
  emit('click', props.friend)
}

const handleContextMenu = (event: MouseEvent) => {
  emit('contextmenu', props.friend, event)
}
</script>

<style scoped>
.friend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.friend-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 12px;
}

.friend-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.friend-item:hover::before {
  opacity: 1;
}

.friend-item.active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.friend-item.active::before {
  opacity: 1;
}

.avatar-wrapper {
  position: relative;
  flex-shrink: 0;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #8ba3f5 0%, #a8c4f8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
  color: #fff;
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.status-dot.online {
  background: #52c41a;
}

.status-dot.offline {
  background: #8c8c8c;
}

.info {
  flex: 1;
  min-width: 0;
  position: relative;
  z-index: 1;
}

.nickname {
  font-size: 15px;
  font-weight: 500;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 2px;
}
</style>