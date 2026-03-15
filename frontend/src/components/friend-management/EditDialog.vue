<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div class="dialog-overlay" v-if="visible" @click="handleClose">
        <div class="dialog-content" @click.stop>
          <div class="dialog-header">
            <h3>编辑好友</h3>
            <button class="close-btn" @click="handleClose">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
              </svg>
            </button>
          </div>

          <div class="dialog-body">
            <!-- 好友信息 -->
            <div class="friend-info-section">
              <div class="avatar">
                {{ displayName.charAt(0).toUpperCase() }}
              </div>
              <div class="info">
                <div class="email">{{ friend?.email }}</div>
                <div class="status" :class="friend?.status">
                  {{ friend?.status === 'online' ? '在线' : '离线' }}
                </div>
              </div>
            </div>

            <!-- 昵称编辑 -->
            <div class="form-group">
              <label>备注昵称</label>
              <input
                v-model="nickname"
                type="text"
                placeholder="输入备注昵称"
                maxlength="20"
              />
            </div>

            <!-- 备注 -->
            <div class="form-group">
              <label>备注信息</label>
              <textarea
                v-model="remark"
                placeholder="添加备注信息..."
                rows="3"
                maxlength="100"
              ></textarea>
            </div>
          </div>

          <div class="dialog-footer">
            <button class="delete-btn" @click="handleDelete">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" fill="currentColor"/>
              </svg>
              删除好友
            </button>
            <div class="actions">
              <button class="cancel-btn" @click="handleClose">取消</button>
              <button class="confirm-btn" @click="handleConfirm" :disabled="saving">
                {{ saving ? '保存中...' : '保存' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import type { Friend } from '@/types/friendTypes'

interface Props {
  visible: boolean
  friend?: Friend
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  confirm: [data: { id: string; nickname: string; remark: string }]
  delete: [id: string]
}>()

const nickname = ref('')
const remark = ref('')
const saving = ref(false)

const displayName = computed(() => props.friend?.nickname || props.friend?.email.split('@')[0] || '')

// 同步数据
watch(() => props.friend, (newFriend) => {
  if (newFriend) {
    nickname.value = newFriend.nickname || ''
    remark.value = newFriend.remark || ''
  }
}, { immediate: true })

const handleClose = () => {
  emit('close')
}

const handleConfirm = async () => {
  if (!props.friend) return

  saving.value = true
  emit('confirm', {
    id: props.friend.id,
    nickname: nickname.value,
    remark: remark.value
  })
  setTimeout(() => {
    saving.value = false
    handleClose()
  }, 300)
}

const handleDelete = () => {
  if (!props.friend) return
  if (confirm('确定要删除该好友吗？')) {
    emit('delete', props.friend.id)
    handleClose()
  }
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  width: 400px;
  max-width: 90vw;
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
}

.dialog-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f5f5;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #eee;
  color: #333;
}

.dialog-body {
  padding: 24px;
}

.friend-info-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f8f9fc;
  border-radius: 12px;
  margin-bottom: 20px;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 600;
  color: #fff;
}

.info .email {
  font-size: 15px;
  font-weight: 500;
  color: #333;
}

.info .status {
  font-size: 13px;
  color: #999;
  margin-top: 4px;
}

.info .status.online {
  color: #52c41a;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #666;
  margin-bottom: 8px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #7494ec;
}

.form-group textarea {
  resize: none;
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #fafafa;
  border-top: 1px solid #eee;
}

.delete-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  background: #fff;
  color: #ff4d4f;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-btn:hover {
  background: #fff1f0;
}

.actions {
  display: flex;
  gap: 12px;
}

.cancel-btn,
.confirm-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #eee;
}

.confirm-btn {
  background: linear-gradient(135deg, #7494ec 0%, #8aa7f0 100%);
  color: #fff;
}

.confirm-btn:hover:not(:disabled) {
  box-shadow: 0 4px 12px rgba(116, 148, 236, 0.4);
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Transition */
.dialog-enter-active,
.dialog-leave-active {
  transition: all 0.3s ease;
}

.dialog-enter-from,
.dialog-leave-to {
  opacity: 0;
}

.dialog-enter-from .dialog-content,
.dialog-leave-to .dialog-content {
  transform: scale(0.9) translateY(20px);
}
</style>