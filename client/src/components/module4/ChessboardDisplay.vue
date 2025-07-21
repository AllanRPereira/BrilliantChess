<template>
  <div class="board-wrapper">
    <TheChessboard
      :board-config="boardConfig"
      @board-created="onBoardCreated"
      @move="onMove"
    />
  </div>
</template>

<script setup>
import { TheChessboard } from 'vue3-chessboard';
import 'vue3-chessboard/style.css';


const emit = defineEmits(['move', 'board-created']);

const boardConfig = {
    coordinates: true,
    movable: {
        free: false // O jogador só pode fazer movimento legais 
    },
    premovable: {
        enabled: false, 
    }
};

// Transmite o movimento feito no tabuleiro 
function onMove(moveData) {
  emit('move', moveData);
}

function onBoardCreated(api) {
    console.log("api criada com sucesso");
    emit('board-created', api);
}
</script>

<style scoped>
.board-wrapper {
  width: 800px;
  max-width: 100%;
  margin: 5px;
}
</style>