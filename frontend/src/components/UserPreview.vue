<template>
    <div class="user-preview-container">
        <div class="avatar-wrapper">
            <img v-if="imageUrl" :src="imageUrl" alt="用户头像" class="avatar-img" />
            <div v-else class="avatar-placeholder">
              {{ nickname ? nickname.charAt(0).toUpperCase() : 'U' }}
            </div>
        </div>

        <div class="item-wrapper">
            <div class="item">{{ nickname }}</div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { computed } from 'vue';
    import { useAuthStore } from '@/stores/authStore';

    // 获取全局状态的用户基本信息
    const authStore = useAuthStore()

    const nickname = computed(() => authStore.nickname)
    const email = computed(() => authStore.email)
    const imageUrl = computed(() => authStore.imageUrl)
</script>

<style scoped>
    .user-preview-container {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .avatar-wrapper {
        flex-shrink: 0;
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid #e0e0e0;
    }

    .avatar-img {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
    }

    .avatar-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #818185;
        color: #fff;
        font-size: 36px;
        font-weight: 600;
        border-radius: 50%;
    }

    .item-wrapper {
        margin-top: 15px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .item {
        display: flex;
        width: 100%;
        color: #333;
        padding-bottom: 5px;
        justify-content: center;
        border-bottom: 1px solid #ccc;
    }
</style>