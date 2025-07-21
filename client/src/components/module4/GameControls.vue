<template>
  <div class="game-controls">
    <button @click="navigate('first')">⏮ Início</button>
    <button @click="navigate('prev')"> << </button>
    <button @click="navigate('next')"> >> </button>
    <button @click="navigate('last')">Fim ⏭</button>
    <button class="reset-button" @click="reset"> Reiniciar</button>
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
  color: #e4b8e4;
  font-weight: 400;
  padding: 8px 16px;
  font-size: 1.3rem;
  border: 3px solid #A772A7;
  background-color: #312433;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}
button:hover {
  background-color: #462b4b;
}
.reset-button {
  background-color: #312433;
  border-color: #A772A7;
  color: #e4b8e4;
}
.reset-button:hover {
  background-color: #462b4b;
}
</style>