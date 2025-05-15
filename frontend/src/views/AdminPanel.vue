<template>
  <v-container v-if="users.length">
    <v-card>
      <v-card-title>Панель администратора</v-card-title>
      <v-card-text>
        <v-table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Имя</th>
              <th>Роль</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.role }}</td>
              <td>
                <v-btn 
                  v-if="user.role !== 'admin'"
                  @click="makeAdmin(user.id)"
                  color="primary"
                  small
                >
                  Сделать админом
                </v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const { fetchApi } = useApi()
const users = ref([])

onMounted(async () => {
  users.value = await fetchApi('/api/users')
})

const makeAdmin = async (userId) => {
  try {
    await fetchApi(`/api/users/${userId}/make_admin`, {
      method: 'POST'
    })
    // Обновляем список пользователей
    users.value = await fetchApi('/api/users')
  } catch (error) {
    console.error('Ошибка:', error)
  }
}
</script>