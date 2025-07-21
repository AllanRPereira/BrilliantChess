<template>
  <div class="game-info">
    <h1 class="game-name">{{ nome }}</h1>
    <p class="game-status">{{ status }}</p>
  </div>
</template>

<script setup>
defineProps({
  nome: { // Nome da partida 
    type: String,
    required: true,
    default: 'Análise de Partida' // Valor padrão caso nada seja passado
  },
  status: {
    type: String,
    required: true,
    default: 'Vez das Brancas' // Valor padrão
  }
});
</script>

<style scoped>
.game-info {
  pointer-events: none;
  text-align: center;
  margin-bottom: 1rem;
  padding: 10px;
  background-color: #312433;
}

.game-name {
  pointer-events: none;
  margin: 0;
  font-size: 1.7em;
  color: #D6B8DA;
}

.game-status {
  pointer-events: none;
  margin: 5px 0 0;
  font-size: 1.1rem;
  font-weight: bold;
  color: #D6B8DA;
}
</style>