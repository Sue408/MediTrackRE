// 好友相关类型定义

export interface Friend {
  id: string
  userId: string // 好友的用户ID
  nickname?: string // 自定义昵称
  avatar?: string // 头像URL
  email: string
  status: 'online' | 'offline'
  remark?: string // 备注
  createdAt: string // 成为好友的时间
}

export interface FriendRequest {
  id: string
  fromUserId: string
  fromNickname: string
  fromAvatar?: string
  fromEmail: string
  status: 'pending' | 'accepted' | 'rejected'
  createdAt: string
}

export interface ChatMessage {
  id: string
  friendId: string // 好友ID
  senderId: string // 发送者ID (自己或好友)
  content: string // 消息内容
  type: 'text' | 'image' | 'system'
  timestamp: string
  isRead: boolean
}

export interface ChatSession {
  friendId: string
  friend: Friend
  lastMessage?: ChatMessage
  unreadCount: number
}

export interface AddFriendRequest {
  email: string
  nickname?: string
}

export interface UpdateFriendRequest {
  id: string
  nickname?: string
  remark?: string
}