import { ref, onUnmounted } from 'vue'
import { io } from 'socket.io-client'
import { useAuthStore } from '@/store/auth'

export const useSocket = () => {
  const authStore = useAuthStore()
  const socket = ref(null)
  const isConnected = ref(false)
  
  const connect = () => {
    socket.value = io('http://localhost:5000', {
      auth: {
        token: authStore.token
      }
    })
    
    socket.value.on('connect', () => {
      isConnected.value = true
    })
    
    socket.value.on('disconnect', () => {
      isConnected.value = false
    })
  }
  
  const disconnect = () => {
    if (socket.value) {
      socket.value.disconnect()
    }
  }
  
  onUnmounted(() => {
    disconnect()
  })
  
  return {
    socket,
    isConnected,
    connect,
    disconnect
  }
}