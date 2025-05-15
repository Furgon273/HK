import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'

export const useApi = () => {
  const authStore = useAuthStore()
  const baseUrl = 'http://localhost:5000/api'
  const error = ref(null)
  const loading = ref(false)

  const fetchApi = async (endpoint, options = {}) => {
    loading.value = true
    error.value = null
    
    try {
      const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
      }
      
      if (authStore.token) {
        headers['Authorization'] = `Bearer ${authStore.token}`
      }
      
      const response = await fetch(`${baseUrl}${endpoint}`, {
        ...options,
        headers,
        credentials: 'same-origin'  // Для работы с куками, если используется
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.message || response.statusText)
      }
      
      return await response.json()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  return { fetchApi, error, loading }
}