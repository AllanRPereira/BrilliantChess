<template>
  <Chessboard :fen="fen" @move="onBoardMove" />
</template>

<script setup>
import { Chessboard } from 'vue-chessboard';
import 'vue-chessboard/dist/vue-chessboard.css';

// Recebe os movimentos 
const props = defineProps({
  fen: {
    type: String,
    required: true,
  },
});


const emit = defineEmits(['move']);

// 3. Quando o tabuleiro da biblioteca emite um evento, nós o retransmitimos para o pai
function onBoardMove(move) {
  emit('move', move);
}
</script>