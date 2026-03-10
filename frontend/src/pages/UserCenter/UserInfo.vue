<template>
    <div class="user-info-container">
        <!-- 顶部用户信息区域 -->
        <div class="wrapper top">
            <transition name="fade-slide" mode="out-in">
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
            </transition>

            <div class="user-base-info">
                <transition name="fade-slide" mode="out-in">
                    <div class="info-item" :key="'nickname'">
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
                </transition>

                <transition name="fade-slide" mode="out-in">
                    <div class="info-item" :key="'email'">
                        <div class="info-item-key">
                            我的邮箱:
                        </div>
                        <div class="info-item-value">
                            {{ email }}
                        </div>
                    </div>
                </transition>

                <transition name="fade-slide" mode="out-in">
                    <div class="info-item" :key="'created'">
                        <div class="info-item-key">
                            注册时间:
                        </div>
                        <div class="info-item-value">
                            {{ formatDate(userCreatedAt) }}
                        </div>
                    </div>
                </transition>
            </div>
        </div>

        <!-- 底部统计区域 -->
        <div class="wrapper down">
            <transition name="bounce" mode="out-in">
                <div class="stats-section" :key="'stats'">
                    <div class="stat-card">
                        <div class="stat-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <path d="M19 3H5C3.89 3 3 4.57 3 6V20C3 21.1 3.89 22 5 22H19C20.1 22 21 21.1 21 20V6C21 4.57 20.1 3 19 3ZM12 6C13.93 6 15.5 7.57 15.5 9.5C15.5 11.43 13.93 13 12 13C10.07 13 8.5 11.43 8.5 9.5C8.5 7.57 10.07 6 12 6ZM6 18V17C6 15 10 13.9 12 13.9C14 13.9 18 15 18 17V18H6Z" fill="currentColor"/>
                            </svg>
                        </div>
                        <div class="stat-info">
                            <span class="stat-value">0</span>
                            <span class="stat-label">用药计划</span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <path d="M4.22 11.29L11.29 4.22C11.68 3.83 12.32 3.83 12.71 4.22L19.78 11.29C20.17 11.68 20.17 12.32 19.78 12.71L12.71 19.78C12.32 20.17 11.68 20.17 11.29 19.78L4.22 12.71C3.83 12.32 3.83 11.68 4.22 11.29Z" fill="currentColor"/>
                                <circle cx="12" cy="12" r="3" fill="currentColor"/>
                            </svg>
                        </div>
                        <div class="stat-info">
                            <span class="stat-value">0</span>
                            <span class="stat-label">药品数量</span>
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-icon">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                                <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5C13.65 5 12 6.65 12 9S13.65 13 16 13ZM8 11C9.66 11 11 9.66 11 8S9.66 5 8 5 5 6.34 5 8 6.34 11 8 11ZM8 13C5.67 13 1 14.17 1 16.5V19H15V16.5C15 14.17 10.33 13 8 13ZM16 13C15.71 13 15.38 13.02 15.03 13.05C16.19 13.89 17 15.02 17 16.5V19H23V16.5C23 14.17 18.33 13 16 13Z" fill="currentColor"/>
                            </svg>
                        </div>
                        <div class="stat-info">
                            <span class="stat-value">0</span>
                            <span class="stat-label">家庭成员</span>
                        </div>
                    </div>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, computed, nextTick } from 'vue';
    import { useAuthStore } from '@/stores/authStore';

    // 获取全局状态的用户基本信息
    const authStore = useAuthStore()

    const nickname = computed(() => authStore.nickname)
    const email = computed(() => authStore.email)
    const imageUrl = computed(() => authStore.imageUrl)

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
                await authStore.updateUserInfo({
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
            await authStore.updateUserInfo({
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
    .user-info-container {
        height: 100%;
        width: 100%;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }

    .wrapper {
        width: 100%;
    }

    .wrapper.top {
        min-height: 200px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        padding: 30px 40px;
        gap: 40px;
    }

    .wrapper.down {
        flex: 1;
        padding: 30px 40px;
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

    /* 用户基本信息 */
    .user-base-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 18px;
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

    /* 统计区域 */
    .stats-section {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }

    .stat-card {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 20px;
        background: #fff;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(116, 148, 236, 0.2);
    }

    .stat-icon {
        width: 50px;
        height: 50px;
        border-radius: 15px;
        background: linear-gradient(135deg, #e8f0ff, #d4e4ff);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #7494ec;
    }

    .stat-info {
        display: flex;
        flex-direction: column;
    }

    .stat-value {
        font-size: 24px;
        font-weight: 700;
        color: #333;
    }

    .stat-label {
        font-size: 13px;
        color: #999;
    }

    /* 动画 - 淡入滑动 */
    .fade-slide-enter-active,
    .fade-slide-leave-active {
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .fade-slide-enter-from {
        opacity: 0;
        transform: translateX(-20px);
    }

    .fade-slide-leave-to {
        opacity: 0;
        transform: translateX(20px);
    }

    /* 动画 - 弹跳 */
    .bounce-enter-active {
        animation: bounce-in 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .bounce-leave-active {
        animation: bounce-out 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }

    @keyframes bounce-in {
        0% {
            opacity: 0;
            transform: scale(0.8);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }

    @keyframes bounce-out {
        0% {
            opacity: 1;
            transform: scale(1);
        }
        100% {
            opacity: 0;
            transform: scale(0.8);
        }
    }

    /* 响应式 */
    @media (max-width: 650px) {
        .wrapper.top {
            flex-direction: column;
            padding: 20px;
            gap: 20px;
        }

        .wrapper.down {
            padding: 20px;
        }

        .stats-section {
            grid-template-columns: 1fr;
        }

        .info-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 8px;
        }

        .info-item-value {
            width: 100%;
        }

        .nickname-edit {
            flex-wrap: wrap;
        }

        .nickname-edit input {
            width: 100%;
        }
    }
</style>
