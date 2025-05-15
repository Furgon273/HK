<template>
  <v-container style="max-width: 800px;">
    <v-card>
      <v-card-title>Добавить забег</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitRun">
          <v-select
            v-model="form.challenge_id"
            :items="challenges"
            item-title="name"
            item-value="id"
            label="Выберите челлендж"
            required
          ></v-select>
          
          <v-text-field
            v-model="form.video_url"
            label="Ссылка на видео (YouTube)"
            required
          ></v-text-field>
          
          <v-textarea
            v-model="form.description"
            label="Описание"
            rows="3"
          ></v-textarea>
          
          <v-btn 
            type="submit" 
            color="primary" 
            :loading="loading"
            block
          >
            Отправить на модерацию
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useApi } from '@/composables/useApi'

const { fetchApi, loading, error } = useApi()
const router = useRouter()

const form = ref({
  challenge_id: null,
  video_url: '',
  description: ''
})

const challenges = ref([])

onMounted(async () => {
  challenges.value = await fetchApi('/challenges')
})

const submitRun = async () => {
  try {
    await fetchApi('/runs', {
      method: 'POST',
      body: JSON.stringify(form.value),
    })
    router.push('/')
  } catch (err) {
    console.error('Error submitting run:', err)
  }
}
</script>