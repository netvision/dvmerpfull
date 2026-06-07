import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin: state => ['hm', 'principal', 'super_admin'].includes(state.user?.role),
    isSuperAdmin: state => state.user?.role === 'super_admin',
  },
  actions: {
    async login(email, password) {
      const form = new URLSearchParams()
      form.append('username', email)
      form.append('password', password)
      const { data } = await api.post('/api/portal/auth/login', form)
      this.token = data.access_token
      localStorage.setItem('token', data.access_token)
      await this.fetchMe()
    },
    async fetchMe() {
      const { data } = await api.get('/api/portal/auth/me')
      this.user = data
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
  },
})
