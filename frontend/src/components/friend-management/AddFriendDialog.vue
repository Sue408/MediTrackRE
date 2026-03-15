<template>
  <Teleport to="body">
    <Transition name="dialog">
      <div class="dialog-overlay" v-if="visible" @click="handleClose">
        <div class="dialog-content" @click.stop>
          <div class="dialog-header">
            <h3>添加好友</h3>
            <button class="close-btn" @click="handleClose">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="currentColor"/>
              </svg>
            </button>
          </div>

          <div class="dialog-body">
            <div class="form-group">
              <label>对方邮箱</label>
              <input
                v-model="email"
                type="email"
                placeholder="输入对方邮箱地址"
              />
            </div>

            <div class="form-group">
              <label>备注昵称（可选）</label>
              <input
                v-model="nickname"
                type="text"
                placeholder="添加备注昵称"
                maxlength="20"
              />
            </div>
          </div>

          <div class="dialog-footer">
            <button class="cancel-btn" @click="handleClose">取消</button>
            <button class="confirm-btn" @click="handleConfirm" :disabled="!email.trim() || adding">
              {{ adding ? '添加中...' : '添加好友' }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  visible: boolean
}

const props = defineProps<Props>()

const emit = defineEmits<{
  close: []
  confirm: [data: { email: string; nickname?: string }]
}>()

const email = ref('')
const nickname = ref('')
const adding = ref(false)

const handleClose = () => {
  email.value = ''
  nickname.value = ''
  emit('close')
}

const handleConfirm = async () => {
  const emailValue = email.value.trim()
  if (!emailValue) return

  adding.value = true
  emit('confirm', {
    email: emailValue,
    nickname: nickname.value || undefined
  })
  setTimeout(() => {
    adding.value = false
    handleClose()
  }, 300)
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

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #666;
  margin-bottom: 8px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #7494ec;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background: #fafafa;
  border-top: 1px solid #eee;
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