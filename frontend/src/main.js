import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { createPinia } from 'pinia'
import App from './App.vue'
import router, { setupRouter } from './router'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
  },
})

const app = createApp(App)
const pinia = createPinia()

app.use(vuetify)
app.use(pinia)

// Создаем хранилище и добавляем его в глобальные свойства
import { useAuthStore } from '@/store/auth'
const authStore = useAuthStore()
app.config.globalProperties.$authStore = authStore

// Настраиваем роутер после инициализации хранилища
app.use(setupRouter(app))

app.mount('#app')