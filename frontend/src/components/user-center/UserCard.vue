<template>
    <div class="user-card-container">
        <!-- 头像区域 -->
        <div class="avatar-section" :key="'avatar'">
            <div class="avatar-wrapper" @click="triggerAvatarUpload">
                <img v-if="imageUrl" :src="imageUrl" alt="用户头像" class="avatar-img" />
                <div v-else class="avatar-placeholder">
                    {{ nickname ? nickname.charAt(0).toUpperCase() : 'U' }}
                </div>
                <div class="avatar-overlay">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                        <circle cx="12" cy="13" r="4"/>
                    </svg>
                </div>
            </div>
            <input
                ref="avatarInput"
                type="file"
                accept="image/*"
                class="avatar-input"
                @change="handleAvatarChange"
            />
        </div>

        <!-- 用户信息 -->
         <div class="user-info">
            <!-- 昵称 -->
            <div class="info-item">
                <div class="info-item-key">
                    我的昵称:
                </div>
                <div class="info-item-value" v-if="!isEditingNickname" @click="startEditNickname">
                    {{ nickname }}
                    <svg class="edit-icon" width="14" height="14" viewBox="0 0 24 24" fill="none">
                        <path d="M3 17.25V21H6.75L17.81 9.94L14.06 6.19L3 17.25ZM20.71 7.04C21.1 6.65 21.1 6.02 20.71 5.63L18.37 3.29C17.98 2.9 17.35 2.9 16.96 3.29L15.13 5.12L18.88 8.87L20.71 7.04Z" fill="currentColor"/>
                    </svg>
                </div>
                <div v-else class="nickname-edit">
                    <input
                        ref="nicknameInput"
                        v-model="editingNickname"
                        type="text"
                        maxlength="20"
                        @keyup.enter="saveNickname"
                        @keyup.escape="cancelEditNickname"
                    />
                    <button class="save-btn" @click="saveNickname" :disabled="savingNickname">
                        {{ savingNickname ? '保存中...' : '保存' }}
                    </button>
                    <button class="cancel-btn" @click="cancelEditNickname">
                        取消
                    </button>
                </div>
            </div>

            <!-- 邮箱 -->
             <div class="info-item" :key="'email'">
                <div class="info-item-key">
                    我的邮箱:
                </div>
                <div class="info-item-value">
                    {{ email }}
                </div>
            </div>

            <!-- 注册时间 -->
             <div class="info-item" :key="'created'">
                <div class="info-item-key">
                    注册时间:
                </div>
                <div class="info-item-value">
                    {{ formatDate(userCreatedAt) }}
                </div>
            </div>
         </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
    import { useUserStore } from '@/stores/userStore';

    // 获取全局状态的用户基本信息
    const userStore = useUserStore()

    const nickname = computed(() => userStore.nickname)
    const email = computed(() => userStore.email)
    const imageUrl = computed(() => userStore.imageUrl)

    // 头像上传
    const avatarInput = ref<HTMLInputElement | null>(null)

    // 编辑昵称
    const isEditingNickname = ref(false)
    const editingNickname = ref('')
    const nicknameInput = ref<HTMLInputElement | null>(null)
    const savingNickname = ref(false)

    function triggerAvatarUpload() {
        avatarInput.value?.click()
    }

    async function handleAvatarChange(event: Event) {
        const target = event.target as HTMLInputElement
        const file = target.files?.[0]
        if (!file) return

        // 检查文件大小（最大2MB）
        if (file.size > 2 * 1024 * 1024) {
            alert('图片大小不能超过2MB')
            return
        }

        const reader = new FileReader()
        reader.onload = async (e) => {
            const base64 = e.target?.result as string
            try {
                await userStore.updateUserInfo({
                    avatar: base64
                })
            } catch (error) {
                console.error('更新头像失败:', error)
            }
        }
        reader.readAsDataURL(file)
        target.value = ''
    }

    function startEditNickname() {
        editingNickname.value = nickname.value
        isEditingNickname.value = true
        nextTick(() => {
            nicknameInput.value?.focus()
        })
    }

    async function saveNickname() {
        if (!editingNickname.value.trim()) {
            alert('昵称不能为空')
            return
        }
        if (editingNickname.value === nickname.value) {
            cancelEditNickname()
            return
        }

        savingNickname.value = true
        try {
            await userStore.updateUserInfo({
                nickname: editingNickname.value.trim()
            })
            isEditingNickname.value = false
        } catch (error) {
            console.error('更新昵称失败:', error)
        } finally {
            savingNickname.value = false
        }
    }

    function cancelEditNickname() {
        isEditingNickname.value = false
        editingNickname.value = ''
    }

    function formatDate(dateStr?: string) {
        if (!dateStr) return '-'
        const date = new Date(dateStr)
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })
    }

    // 注册时间 - 使用登录时返回的创建时间
    const userCreatedAt = ref('')
</script>

<style scoped>
    .user-card-container {
        height: 100%;
        width: 100%;
        display: flex;
        align-items: center;
        padding: 25px 30px;
        gap: 30px;
    }

    /* 头像区域 */
    .avatar-section {
        flex-shrink: 0;
    }

    .avatar-wrapper {
        position: relative;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        overflow: hidden;
        cursor: pointer;
        border: 4px solid #e8e8e8;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .avatar-wrapper:hover {
        border-color: #7494ec;
        transform: scale(1.08);
        box-shadow: 0 8px 25px rgba(116, 148, 236, 0.3);
    }

    .avatar-wrapper:hover .avatar-overlay {
        opacity: 1;
    }

    .avatar-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .avatar-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #7494ec, #9bb5f5);
        color: #fff;
        font-size: 42px;
        font-weight: 600;
    }

    .avatar-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .avatar-overlay svg {
        width: 36px;
        height: 36px;
        color: #fff;
    }

    .avatar-input {
        display: none;
    }

    /* 用户信息 */
    .user-info {
        flex: 1;
        display: flex;
        flex-direction: column;
    }

    .info-item {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .info-item-key {
        color: #666;
        font-size: 15px;
        min-width: 80px;
    }

    .info-item-value {
        font-size: 16px;
        color: #333;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        padding: 6px 12px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .info-item-value:hover {
        background: #f5f8ff;
    }

    .edit-icon {
        opacity: 0;
        transition: opacity 0.3s ease;
        color: #7494ec;
    }

    .info-item-value:hover .edit-icon {
        opacity: 1;
    }

    .nickname-edit {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .nickname-edit input {
        padding: 8px 15px;
        border: 2px solid #7494ec;
        border-radius: 10px;
        font-size: 15px;
        outline: none;
        width: 180px;
        transition: all 0.3s ease;
    }

    .nickname-edit input:focus {
        box-shadow: 0 0 0 4px rgba(116, 148, 236, 0.2);
    }

    .save-btn,
    .cancel-btn {
        padding: 8px 16px;
        border: none;
        border-radius: 8px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
    }

.save-btn {
        background: #7494ec;
        color: #fff;
    }

    .save-btn:hover:not(:disabled) {
        background: #5a7de0;
    }

    .save-btn:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }

    .cancel-btn {
        background: #f5f5f5;
        color: #666;
    }

    .cancel-btn:hover {
        background: #e8e8e8;
    }
</style>