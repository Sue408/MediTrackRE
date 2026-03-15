<template>
  <div class="auth-container">
    <div class="auth-box" :class="{ active: isActive }">
      <div class="form-box login">
        <AuthForm
          :is-login="true"
          :loading="loginLoading"
          :button-error="loginButtonError"
          @submit="handleLogin"
        />
      </div>

      <div class="form-box register">
        <AuthForm
          :is-login="false"
          :loading="registerLoading"
          :button-error="registerButtonError"
          @submit="handleRegister"
        />
      </div>

      <div class="toggle-box">
        <div class="toggle-panel toggle-left">
          <h1>欢迎回来！</h1>
          <p>还没有账户？</p>
          <button class="btn register-btn" @click="toggle(true)">前往注册</button>
        </div>

        <div class="toggle-panel toggle-right">
          <h1>您好！</h1>
          <p>已有账户？</p>
          <button class="btn login-btn" @click="toggle(false)">前往登录</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AuthForm from '@/components/auth/AuthForm.vue'
import { useUserStore } from '@/stores/userStore'
import { register as registerApi } from '@/api/auth'
import { extractErrorMessage } from '@/utils/error'

const router = useRouter()
const authStore = useUserStore()

const isActive = ref(false)
const loginLoading = ref(false)
const registerLoading = ref(false)
const loginButtonError = ref('')
const registerButtonError = ref('')

const toggle = (state: boolean) => {
  isActive.value = state
  loginButtonError.value = ''
  registerButtonError.value = ''
}

const clearButtonError = (isLogin: boolean) => {
  setTimeout(() => {
    if (isLogin) {
      loginButtonError.value = ''
    } else {
      registerButtonError.value = ''
    }
  }, 1000)
}

const handleLogin = async (data: { email: string; password: string }) => {
  loginLoading.value = true
  loginButtonError.value = ''

  try {
    await authStore.login({
      email: data.email,
      password: data.password
    })
    router.replace({ name: 'Home' })
  } catch (error: unknown) {
    const message = extractErrorMessage(error)
    loginButtonError.value = message
    clearButtonError(true)
  } finally {
    loginLoading.value = false
  }
}

const handleRegister = async (data: { email: string; password: string; username?: string }) => {
  if (!data.username) {
    registerButtonError.value = '请输入昵称'
    clearButtonError(false)
    return
  }

  registerLoading.value = true
  registerButtonError.value = ''

  try {
    await registerApi({
      nickname: data.username,
      email: data.email,
      password: data.password
    })
    isActive.value = false
  } catch (error: unknown) {
    const message = extractErrorMessage(error)
    registerButtonError.value = message
    clearButtonError(false)
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(90deg, #e2e2e2, #c9d6ff);
}

.auth-box {
  width: 750px;
  height: 450px;
  position: relative;
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.form-box {
  position: absolute;
  right: 0;
  width: 50%;
  height: 100%;
  background-color: #fff;
  display: flex;
  align-items: center;
  text-align: center;
  color: #333;
  padding: 40px;
}

.form-box.register {
  right: 50%;
  visibility: hidden;
}

.auth-box.active .form-box.register {
  visibility: visible;
}

.toggle-box {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.toggle-box::before {
  content: '';
  position: absolute;
  left: -250%;
  width: 300%;
  height: 100%;
  background-color: #7494ec;
  z-index: 2;
  border-radius: 120px;
  transition: 1.8s ease-in-out;
}

.auth-box.active .toggle-box::before {
  left: 50%;
}

.toggle-panel {
  position: absolute;
  width: 50%;
  height: 100%;
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2;
  transition: 0.6s ease-in-out;
}

.toggle-panel.toggle-left {
  left: 0;
  transition-delay: 1.2s;
}

.toggle-panel.toggle-right {
  right: -50%;
  transition-delay: 0.6s;
}

.auth-box.active .toggle-panel.toggle-left {
  left: -50%;
  transition-delay: 0.6s;
}

.auth-box.active .toggle-panel.toggle-right {
  right: 0;
  transition-delay: 1.2s;
}

.toggle-panel p {
  margin-bottom: 20px;
}

.toggle-panel .btn {
  width: 160px;
  height: 46px;
  background-color: transparent;
  border: 2px solid #fff;
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  box-shadow: none;
  pointer-events: auto;
}

.toggle-panel .btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

@media screen and (max-width: 650px) {
  .auth-box {
    height: calc(100vh - 40px);
  }

  .form-box {
    bottom: 0;
    width: 100%;
    height: 70%;
  }

  .auth-box.active .form-box {
    right: 0;
    bottom: 30%;
  }

  .toggle-box::before {
    left: 0;
    width: 100%;
    top: -270%;
    height: 300%;
    border-radius: 20vw;
  }

  .auth-box.active .toggle-box::before {
    left: 0;
    top: 70%;
  }

  .toggle-panel {
    width: 100%;
    height: 30%;
  }

  .toggle-panel.toggle-left {
    top: 0;
  }

  .auth-box.active .toggle-panel.toggle-left {
    left: 0;
    top: -30%;
  }

  .toggle-panel.toggle-right {
    right: 0;
    bottom: -30%;
  }

  .auth-box.active .toggle-panel.toggle-right {
    bottom: 0;
  }
}

@media screen and (max-width: 400px) {
  .form-box {
    padding: 20px;
  }

  .toggle-panel h1 {
    font-size: 30px;
  }
}
</style>
