<template>
  <div class="game-controls">
    <button @click="navigate('first')">⏮️ Início</button>
    <button @click="navigate('prev')"> << </button>
    <button @click="navigate('next')"> >> </button>
    <button @click="navigate('last')">Fim ⏭️</button>
    <button class="reset-button" @click="reset">🔄 Reiniciar</button>
  </div>
</template>

<script setup>
const emit = defineEmits(['navigate', 'reset']);


function navigate(direction) {
  emit('navigate', direction);
}

function reset() {
  emit('reset');
}
</script>

<style scoped>

.game-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
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