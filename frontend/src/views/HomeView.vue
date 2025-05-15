<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const { fetchApi, error, loading } = useApi()
const recentRuns = ref([])
const recentDiscussions = ref([])

onMounted(async () => {
  try {
    const response = await fetchApi('/runs?limit=5')
    recentRuns.value = response || []
    recentDiscussions.value = await fetchApi('/discussions?limit=5')
  } catch (err) {
    console.error('Ошибка загрузки данных:', err)
    // Можно показать уведомление пользователю
  }
})
</script>