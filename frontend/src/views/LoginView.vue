<template>
  <v-container class="fill-height" style="max-width: 400px;">
    <v-card class="pa-4">
      <v-card-title>Вход</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleLogin">
          <v-text-field
            v-model="username"
            label="Никнейм"
            required
          ></v-text-field>
          
          <v-text-field
            v-model="password"
            label="Пароль"
            type="password"
            required
          ></v-text-field>
          
          <v-btn 
            type="submit" 
            color="primary" 
            block 
            :loading="loading"
          >
            Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  try {
    loading.value = true
    const success = await authStore.login(username.value, password.value)
    if (success) {
      router.push('/')
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>