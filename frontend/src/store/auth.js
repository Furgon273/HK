import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const { fetchApi } = useApi()
  
  const token = ref(localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user')))
  const isAuthenticated = computed(() => !!token.value)

  const login = async (username, password) => {
    try {
      const data = await fetchApi('/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      })
      
      token.value = data.access_token
      user.value = { username: data.username, role: data.role }
      
      localStorage.setItem('token', data.access_token)
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return true
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/login')
  }

  return { 
    token, 
    user, 
    isAuthenticated, 
    login, 
    logout 
  }
})