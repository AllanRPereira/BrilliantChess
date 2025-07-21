<template>
  <div class="board-wrapper">
    <TheChessboard
      :fen="fen"
      :board-config="boardConfig"
      @move="onMove"
    />
  </div>
</template>

<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';

// As props que o nosso componente vai aceitar do pai (Module4View)
defineProps({
  fen: {
    type: String,
    required: true
  },
  lastMove: {
    type: Array,
    required: false
  }
});

const emit = defineEmits(['move']);

const boardConfig = {
    coordinates: true,
  movable: {
    free: false // O jogador só pode mover as peças da vez
  }
};

// Quando um movimento é feito no tabuleiro, esta função é chamada.
function onMove(moveData) {
  // Apenas retransmite o evento 'move' para o componente pai.
  // A biblioteca já valida se o movimento é legal.
  emit('move', moveData);
}
</script>

<style scoped>
.board-wrapper {
  width: 800px;
  max-width: 100%;
}
</style>