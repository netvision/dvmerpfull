import { reactive, computed } from 'vue'
import apiClient from '../config/api'

interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: string
  is_active: boolean
}

interface AuthState {
  user: User | null
  accessToken: string | null
  loading: boolean
}

const state = reactive<AuthState>({
  user: null,
  accessToken: null,
  loading: false
})

export const authStore = {
  state,
  
  isAuthenticated: computed(() => !!state.accessToken && !!state.user),
  isAdmin: computed(() => state.user?.role === 'admin'),

  initializeFromStorage() {
    const storedToken = localStorage.getItem('websiteAccessToken')
    const storedUser = localStorage.getItem('websiteUser')

    if (storedToken && storedUser) {
      state.accessToken = storedToken
      state.user = JSON.parse(storedUser)
    }
  },

  async login(email: string, password: string) {
    state.loading = true
    try {
      const response = await apiClient.post('/core/auth/login', { email, password })
      
      state.user = response.data.data.user
      state.accessToken = response.data.data.accessToken

      localStorage.setItem('websiteAccessToken', response.data.data.accessToken)
      localStorage.setItem('websiteUser', JSON.stringify(response.data.data.user))

      return response.data
    } catch (error: any) {
      throw error
    } finally {
      state.loading = false
    }
  },

  logout() {
    state.user = null
    state.accessToken = null
    localStorage.removeItem('websiteAccessToken')
    localStorage.removeItem('websiteUser')
  }
}
