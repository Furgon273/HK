<template>
  <v-app-bar app color="primary">
    <v-toolbar-title>HK Leaderboard</v-toolbar-title>
    <v-spacer></v-spacer>
    
    <v-btn to="/" text>Главная</v-btn>
    <v-btn to="/leaderboard" text>Топ игроков</v-btn>
    <v-btn 
        v-if="authStore.user?.role === 'admin'"
        to="/admin"
        text
        >
        Админ-панель
    </v-btn>
    
    <template v-if="!authStore.isAuthenticated">
      <v-btn to="/login" text>Войти</v-btn>
      <v-btn to="/register" text>Регистрация</v-btn>
    </template>
    
    <template v-else>
      <v-btn to="/submit-run" text>Добавить забег</v-btn>
      <v-btn :to="`/profile/${authStore.user.username}`" text>
        <v-icon left>mdi-account</v-icon>
        {{ authStore.user.username }}
      </v-btn>
      <v-btn @click="authStore.logout()" text>Выйти</v-btn>
    </template>
  </v-app-bar>
</template>

<script setup>
import { useAuthStore } from '@/store/auth'
const authStore = useAuthStore()
</script>