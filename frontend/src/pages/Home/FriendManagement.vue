<template>
  <div class="friend-management-container">
    <!-- 侧边栏 -->
    <div class="control-wrapper">
      <div class="top-panel">
        <button class="back-btn" @click="backHome">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15.41 7.41L14 6L8 12L14 18L15.41 16.59L10.83 12L15.41 7.41Z" fill="currentColor"/>
          </svg>
        </button>
        <h3>好友管理</h3>
      </div>
      <div class="side-bar-panel">
        <FriendList
          :friends="friends"
          :selected-friend-id="selectedFriend?.id"
          @select="handleSelectFriend"
          @contextmenu="handleContextMenu"
          @addfriend="showAddFriendDialog = true"
        />
      </div>
    </div>

    <!-- 内容区 -->
    <div class="content-wrapper">
      <ChatPanel
        :selected-friend="selectedFriend"
        :messages="messages"
        :sending="sending"
        @send="handleSendMessage"
      />
    </div>

    <!-- 编辑弹窗 -->
    <EditDialog
      :visible="showEditDialog"
      :friend="editingFriend"
      @close="closeEditDialog"
      @confirm="handleConfirmEdit"
      @delete="handleDeleteFriend"
    />

    <!-- 添加好友弹窗 -->
    <AddFriendDialog
      :visible="showAddFriendDialog"
      @close="showAddFriendDialog = false"
      @confirm="handleAddFriend"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import type { Friend, ChatMessage } from '@/types/friendTypes'
import { getFriendList, getChatHistoryByFriendId, sendMessage, updateFriend, removeFriend, addFriend } from '@/api/friend'
import FriendList from '@/components/friend-management/FriendList.vue'
import ChatPanel from '@/components/friend-management/ChatPanel.vue'
import EditDialog from '@/components/friend-management/EditDialog.vue'
import AddFriendDialog from '@/components/friend-management/AddFriendDialog.vue'

const router = useRouter()

// 状态
const friends = ref<Friend[]>([])
const selectedFriend = ref<Friend | undefined>()
const messages = ref<ChatMessage[]>([])
const sending = ref(false)
const showEditDialog = ref(false)
const editingFriend = ref<Friend | undefined>()
const showAddFriendDialog = ref(false)

// 返回首页
const backHome = () => {
  router.replace('/')
}

// 加载好友列表
const loadFriends = async () => {
  try {
    friends.value = await getFriendList()
  } catch (error) {
    console.error('加载好友列表失败:', error)
  }
}

// 选择好友
const handleSelectFriend = async (friend: Friend) => {
  selectedFriend.value = friend
  try {
    messages.value = await getChatHistoryByFriendId(friend.id)
  } catch (error) {
    console.error('加载聊天记录失败:', error)
    messages.value = []
  }
}

// 右键菜单
const handleContextMenu = (friend: Friend, _event: MouseEvent) => {
  editingFriend.value = friend
  showEditDialog.value = true
}

// 关闭编辑弹窗
const closeEditDialog = () => {
  showEditDialog.value = false
  editingFriend.value = undefined
}

// 确认编辑
const handleConfirmEdit = async (data: { id: string; nickname: string; remark: string }) => {
  try {
    await updateFriend({ id: data.id, nickname: data.nickname, remark: data.remark })
    // 更新本地列表
    await loadFriends()
  } catch (error) {
    console.error('更新好友失败:', error)
  }
}

// 删除好友
const handleDeleteFriend = async (id: string) => {
  try {
    await removeFriend(id)
    // 如果删除的是当前选中的好友，清空选择
    if (selectedFriend.value?.id === id) {
      selectedFriend.value = undefined
      messages.value = []
    }
    // 刷新列表
    await loadFriends()
  } catch (error) {
    console.error('删除好友失败:', error)
  }
}

// 添加好友
const handleAddFriend = async (data: { email: string; nickname?: string }) => {
  try {
    await addFriend(data)
    showAddFriendDialog.value = false
    // 刷新列表
    await loadFriends()
  } catch (error) {
    console.error('添加好友失败:', error)
  }
}

// 发送消息
const handleSendMessage = async (content: string) => {
  if (!selectedFriend.value) return

  sending.value = true
  try {
    const newMessage = await sendMessage(selectedFriend.value.id, content)
    messages.value.push(newMessage)
  } catch (error) {
    console.error('发送消息失败:', error)
  } finally {
    sending.value = false
  }
}

// 初始化
onMounted(() => {
  loadFriends()
})
</script>

<style scoped>
.friend-management-container {
  width: 100%;
  height: 100%;
  display: flex;
}

.control-wrapper {
  height: 100%;
  width: 25%;
  min-width: 280px;
  user-select: none;
  background: linear-gradient(160deg, #6b8cf5 0%, #7d9cf0 40%, #8aa7f0 80%, #9bb3f0 100%);
  position: relative;
  overflow: hidden;
}

/* 侧边栏底部装饰 */
.control-wrapper::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120px;
  background: linear-gradient(to top, rgba(255,255,255,0.08) 0%, transparent 100%);
  pointer-events: none;
}

/* 顶部装饰圆点 */
.control-wrapper::before {
  content: '';
  position: absolute;
  top: -30px;
  right: -30px;
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  pointer-events: none;
}

.top-panel {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 10px;
  color: #fff;
  padding: 20px 25px;
}

.back-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  border: none;
  transition: all 0.6s ease;
  cursor: pointer;
}

.back-btn:hover {
  background-color: #fff;
  transform: scale(1.2);
}

.side-bar-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 15px;
  height: calc(100% - 80px);
}

.content-wrapper {
  padding: 10px;
  width: 75%;
  overflow: hidden;
  position: relative;
  min-height: 500px;
}
</style>