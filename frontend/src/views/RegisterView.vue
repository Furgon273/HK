<template>
  <v-container class="fill-height" style="max-width: 400px;">
    <v-card class="pa-4">
      <v-card-title class="text-center">Регистрация</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="handleRegister">
          <v-text-field
            v-model="form.username"
            label="Никнейм"
            :error-messages="errors.username"
            required
            outlined
          ></v-text-field>
          
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            :error-messages="errors.email"
            required
            outlined
          ></v-text-field>
          
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            :error-messages="errors.password"
            required
            outlined
          ></v-text-field>
          
          <v-text-field
            v-model="form.password_confirmation"
            label="Подтверждение пароля"
            type="password"
            :error-messages="errors.password_confirmation"
            required
            outlined
          ></v-text-field>
          
          <v-btn 
            type="submit" 
            color="primary" 
            block 
            :loading="loading"
            size="large"
          >
            Зарегистрироваться
          </v-btn>
          
          <div class="text-center mt-4">
            Уже есть аккаунт? <router-link to="/login">Войти</router-link>
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'

const router = useRouter()
const { fetchApi } = useApi()

const form = ref({
  username: '',
  email: '',
  password: '',
  password_confirmation: ''
})

const errors = ref({})
const loading = ref(false)

const validate = () => {
  errors.value = {}
  let valid = true

  if (!form.value.username) {
    errors.value.username = 'Введите никнейм'
    valid = false
  }

  if (!form.value.email) {
    errors.value.email = 'Введите email'
    valid = false
  } else if (!/^\S+@\S+\.\S+$/.test(form.value.email)) {
    errors.value.email = 'Введите корректный email'
    valid = false
  }

  if (!form.value.password) {
    errors.value.password = 'Введите пароль'
    valid = false
  } else if (form.value.password.length < 6) {
    errors.value.password = 'Пароль должен быть не менее 6 символов'
    valid = false
  }

  if (form.value.password !== form.value.password_confirmation) {
    errors.value.password_confirmation = 'Пароли не совпадают'
    valid = false
  }

  return valid
}

const handleRegister = async () => {
  if (!validate()) return

  loading.value = true
  errors.value = {}

  try {
    await fetchApi('/register', {
      method: 'POST',
      body: JSON.stringify(form.value),
    })
    
    router.push('/login')
  } catch (error) {
    if (error.response && error.response.data) {
      errors.value = error.response.data.errors || {}
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}

.v-btn {
  text-transform: none;
  letter-spacing: normal;
}
</style>