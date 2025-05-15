<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Топ игроков</span>
        <v-chip v-if="lastUpdated" color="info">
          Обновлено: {{ lastUpdated.toLocaleTimeString() }}
        </v-chip>
      </v-card-title>
      
      <v-card-text>
        <v-table>
          <thead>
            <tr>
              <th>№</th>
              <th>Ник</th>
              <th>Лига</th>
              <th>Макс. сложность</th>
              <th>Забегов</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(player, index) in leaderboard" :key="player.username">
              <td>{{ index + 1 }}</td>
              <td>
                <router-link :to="`/profile/${player.username}`">
                  {{ player.username }}
                </router-link>
              </td>
              <td>
                <v-chip :color="getLeagueColor(player.league)">
                  {{ player.league }}
                </v-chip>
              </td>
              <td>{{ player.max_difficulty }}</td>
              <td>{{ player.runs_count }}</td>
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
const leaderboard = ref([])
const lastUpdated = ref(null)

const getLeagueColor = (league) => {
  const colors = {
    bronze: 'brown',
    silver: 'grey lighten-1',
    gold: 'amber',
    platinum: 'blue-grey',
    diamond: 'cyan',
  }
  return colors[league.toLowerCase()] || 'primary'
}

onMounted(async () => {
  leaderboard.value = await fetchApi('/leaderboard')
  lastUpdated.value = new Date()
})
</script>