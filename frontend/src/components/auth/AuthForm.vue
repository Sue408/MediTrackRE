<template>
  <form @submit.prevent="handleSubmit" class="auth-form">
    <h1>{{ isLogin ? 'Login' : 'Registeration' }}</h1>

    <div v-if="!isLogin" class="input-box">
      <input
        v-model="formData.username"
        type="text"
        placeholder="昵称"
        required
        :disabled="loading"
      >
      <i class="bx bxs-user"></i>
    </div>

    <div class="input-box">
      <input
        v-model="formData.email"
        type="email"
        placeholder="Email"
        required
        :disabled="loading"
      >
      <i class="bx bxs-envelope"></i>
    </div>

    <div class="input-box">
      <input
        v-model="formData.password"
        type="password"
        placeholder="Password"
        required
        :disabled="loading"
      >
      <i class="bx bxs-lock-alt"></i>
    </div>

    <div v-if="isLogin" class="forgot-link">
      <a href="#">忘记密码？</a>
    </div>

    <button
      type="submit"
      class="btn"
      :class="{ 'btn-error': buttonError }"
      :disabled="loading || !!buttonError"
    >
      <span v-if="loading" class="loading-spinner"></span>
      <span v-else-if="buttonError" class="error-text" :title="buttonError">{{ buttonError }}</span>
      <span v-else>{{ isLogin ? '登录' : '注册' }}</span>
    </button>

    <p>或者使用第三方{{ isLogin ? '登录' : '注册' }}</p>

    <div class="social-icons">
      <a
        v-for="social in socialIcons"
        :key="social.icon"
        href="#"
      >
        <i :class="social.icon"></i>
      </a>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'

interface Props {
  isLogin: boolean
  loading?: boolean
  buttonError?: string
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  buttonError: ''
})

const emit = defineEmits<{
  submit: [data: { email: string; password: string; username?: string }]
}>()

const formData = reactive({
  email: '',
  password: '',
  username: ''
})

const socialIcons = [
  { icon: 'bx bxl-google' },
  { icon: 'bx bxl-facebook' },
  { icon: 'bx bxl-github' },
  { icon: 'bx bxl-linkedin' }
]

const handleSubmit = () => {
  emit('submit', {
    email: formData.email,
    password: formData.password,
    username: props.isLogin ? undefined : formData.username
  })
}

// 1秒后自动清除错误状态
watch(() => props.buttonError, (newError) => {
  if (newError) {
    setTimeout(() => {
      // 这里只是视觉效果清除，实际错误状态由父组件管理
    }, 1000)
  }
})
</script>

<style scoped>
.auth-form {
  width: 100%;
}

.auth-form h1 {
  font-size: 32px;
  margin: -10px 0;
}

.auth-form p {
  font-size: 14px;
  margin: 15px 0;
}

.input-box {
  position: relative;
  margin: 30px 0;
}

.input-box input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  outline: none;
  background-color: #eee;
  border-radius: 8px;
  color: #333;
  font-weight: 500;
  transition: background-color 0.3s;
}

.input-box input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-box input::placeholder {
  color: #888;
  font-weight: 400;
}

.input-box i {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 20px;
  color: #888;
}

.forgot-link {
  margin: -15px 0 15px;
}

.forgot-link a {
  font-size: 14px;
  color: #333;
  text-decoration: none;
}

.btn {
  width: 100%;
  height: 48px;
  background-color: #7494ec;
  border-radius: 8px;
  border: none;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 16px;
  color: #fff;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.btn:hover:not(:disabled) {
  background-color: #5a7de8;
}

.btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-error {
  background-color: #dc2626 !important;
}

.btn-error:hover {
  background-color: #b91c1c !important;
}

.error-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 100%;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.social-icons {
  display: flex;
  justify-content: center;
}

.social-icons a {
  display: inline-flex;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
  font-size: 18px;
  text-decoration: none;
  margin: 0 8px;
  transition: border-color 0.3s, background-color 0.3s;
}

.social-icons a:hover {
  border-color: #7494ec;
  background-color: #f0f4ff;
}
</style>