<script setup>
// Define as propriedades que este componente recebe do pai.
defineProps({
  partida: { type: Object, required: true },
});

// Define os eventos que este componente emite para o pai.
const emit = defineEmits(['ver-analise', 'apagar']);
</script>

<template>
  <li class="game-item">
    <div class="info">
      <span class="nome">{{ partida.nome }}</span>
      <span class="data">Data: {{ new Date(partida.data).toLocaleDateString() }}</span>
    </div>
    <div class="actions">
      <button @click="emit('ver-analise', partida.id)">Ver Análise</button>
      <button @click="emit('apagar', partida.id)" class="delete-btn">Apagar</button>
    </div>
  </li>
</template>

<style scoped>
.game-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid #eee; }
.info { display: flex; flex-direction: column; }
.nome { font-weight: bold; }
.data { font-size: 0.9em; color: #666; }
.delete-btn { background-color: #e74c3c; color: white; border: none; }
</style>