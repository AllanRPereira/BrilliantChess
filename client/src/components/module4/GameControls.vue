<template>
  <div class="game-controls">
    <button @click="emit('navigate', 'first')">⏮️ Início</button>
    <button @click="emit('navigate', 'prev')">⬅️ Anterior</button>
    <button @click="emit('navigate', 'next')">Próximo ➡️</button>
    <button @click="emit('navigate', 'last')">Fim ⏭️</button>
    <button class="reset-button" @click="emit('reset')">🔄 Reiniciar</button>
  </div>
</template>

<script setup>
const emit = defineEmits(['navigate', 'reset']); // Esse componente pode navegar ou resetar a analise
</script>

<style scoped>
.game-controls {
  display: flex;
  justify-content: center;
  gap: 10px; /* Espaço entre os botões */
  margin-top: 1rem;
}

button {
  padding: 8px 16px;
  font-size: 1em;
  border: 1px solid #ccc;
  background-color: #fff;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #f0f0f0;
}

.reset-button {
  background-color: #f2dede;
  border-color: #ebccd1;
  color: #a94442;
}

.reset-button:hover {
  background-color: #e4b9b9;
}
</style>