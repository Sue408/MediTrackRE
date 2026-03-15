// 好友相关 API
import type { Friend, ChatMessage, AddFriendRequest, UpdateFriendRequest } from '@/types/friendTypes'

// Mock 数据存储
const MOCK_FRIENDS: Friend[] = [
  {
    id: '1',
    userId: 'user-001',
    nickname: '张三',
    avatar: '',
    email: 'zhangsan@example.com',
    status: 'online',
    createdAt: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    userId: 'user-002',
    nickname: '李四',
    avatar: '',
    email: 'lisi@example.com',
    status: 'offline',
    createdAt: '2024-02-20T14:30:00Z'
  },
  {
    id: '3',
    userId: 'user-003',
    nickname: '王五',
    avatar: '',
    email: 'wangwu@example.com',
    status: 'online',
    remark: '一起打篮球的朋友',
    createdAt: '2024-03-05T09:15:00Z'
  },
  {
    id: '4',
    userId: 'user-004',
    nickname: '赵六',
    avatar: '',
    email: 'zhaoliu@example.com',
    status: 'offline',
    createdAt: '2024-03-10T16:45:00Z'
  }
]

// 本地存储聊天记录
const getChatHistory = (friendId: string): ChatMessage[] => {
  const key = `chat_history_${friendId}`
  const data = localStorage.getItem(key)
  if (data) {
    return JSON.parse(data)
  }
  // 初始化一些mock聊天记录
  const initialMessages: ChatMessage[] = [
    {
      id: `msg_${friendId}_1`,
      friendId,
      senderId: 'user-001',
      content: '你好！最近身体怎么样？',
      type: 'text',
      timestamp: '2024-03-10T10:00:00Z',
      isRead: true
    },
    {
      id: `msg_${friendId}_2`,
      friendId,
      senderId: 'me',
      content: '挺好的，谢谢关心！你呢？',
      type: 'text',
      timestamp: '2024-03-10T10:05:00Z',
      isRead: true
    },
    {
      id: `msg_${friendId}_3`,
      friendId,
      senderId: 'user-001',
      content: '我也不错~记得按时吃药哦！',
      type: 'text',
      timestamp: '2024-03-10T10:10:00Z',
      isRead: true
    }
  ]
  localStorage.setItem(key, JSON.stringify(initialMessages))
  return initialMessages
}

const saveChatHistory = (friendId: string, messages: ChatMessage[]) => {
  const key = `chat_history_${friendId}`
  localStorage.setItem(key, JSON.stringify(messages))
}

/**
 * 获取好友列表
 */
export const getFriendList = async (): Promise<Friend[]> => {
  // 模拟API延迟
  await new Promise(resolve => setTimeout(resolve, 300))
  return [...MOCK_FRIENDS]
}

/**
 * 添加好友
 */
export const addFriend = async (data: AddFriendRequest): Promise<Friend> => {
  await new Promise(resolve => setTimeout(resolve, 500))

  const newFriend: Friend = {
    id: `friend_${Date.now()}`,
    userId: `user_${Date.now()}`,
    nickname: data.nickname || data.email.split('@')[0],
    email: data.email,
    status: 'offline',
    createdAt: new Date().toISOString()
  }

  MOCK_FRIENDS.push(newFriend)
  return newFriend
}

/**
 * 删除好友
 */
export const removeFriend = async (friendId: string): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 300))

  const index = MOCK_FRIENDS.findIndex(f => f.id === friendId)
  if (index !== -1) {
    MOCK_FRIENDS.splice(index, 1)
  }
}

/**
 * 更新好友信息
 */
export const updateFriend = async (data: UpdateFriendRequest): Promise<Friend> => {
  await new Promise(resolve => setTimeout(resolve, 300))

  const friend = MOCK_FRIENDS.find(f => f.id === data.id)
  if (!friend) {
    throw new Error('好友不存在')
  }

  if (data.nickname !== undefined) {
    friend.nickname = data.nickname
  }
  if (data.remark !== undefined) {
    friend.remark = data.remark
  }

  return { ...friend }
}

/**
 * 获取聊天记录
 */
export const getChatHistoryByFriendId = async (friendId: string): Promise<ChatMessage[]> => {
  await new Promise(resolve => setTimeout(resolve, 200))
  return getChatHistory(friendId)
}

/**
 * 发送消息
 */
export const sendMessage = async (friendId: string, content: string): Promise<ChatMessage> => {
  await new Promise(resolve => setTimeout(resolve, 100))

  const messages = getChatHistory(friendId)

  const newMessage: ChatMessage = {
    id: `msg_${Date.now()}`,
    friendId,
    senderId: 'me',
    content,
    type: 'text',
    timestamp: new Date().toISOString(),
    isRead: true
  }

  messages.push(newMessage)
  saveChatHistory(friendId, messages)

  return newMessage
}
