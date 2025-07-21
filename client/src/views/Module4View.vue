<template>
  <div v-if="!partida" class="loading-container">
    <p>Carregando análise da partida...</p>
  </div>

  <div v-else class="game-view-container">
    <div class="game-layout">
      <div class="main-column">
        <GameInfo :nome="partida.nome" :status="gameStatus" />
        <ChessboardDisplay :fen="boardFen" :last-move="currentLastMove" @move="handleMove" />
        <GameControls @reset="resetGame" @navigate="handleNavigate" />
      </div>
      <MoveHistory 
          :analyzedMoves="partida.analyzedMoves"
          :currentEvaluation="currentEval"
          :activeMoveIndex="activeMoveIndex"
          @select-move="goToMove"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { Chess } from 'chess.js';
import { fetchGameById } from '../services/apiService.js';

import GameInfo from '../components/module4/GameInfo.vue';
import ChessboardDisplay from '../components/module4/ChessboardDisplay.vue';
import MoveHistory from '../components/module4/MoveHistory.vue';
import GameControls from '../components/module4/GameControls.vue';

// --- ESTADO ---
const route = useRoute();
const game = new Chess();
const partida = ref(null);
const boardFen = ref('');
const activeMoveIndex = ref(-1);

// --- PROPRIEDADES COMPUTADAS ---
const currentLastMove = computed(() => {
  if (activeMoveIndex.value < 0 || !partida.value?.analyzedMoves) {
    return undefined;
  }
  const tempGame = new Chess();
  if (partida.value.fenInicial) {
    tempGame.load(partida.value.fenInicial);
  }
  for (let i = 0; i < activeMoveIndex.value; i++) {
    tempGame.move(partida.value.analyzedMoves[i].san);
  }
  const activeMoveData = tempGame.move(partida.value.analyzedMoves[activeMoveIndex.value].san);
  if (activeMoveData) {
    return [activeMoveData.from, activeMoveData.to];
  }
  return undefined;
});

const gameStatus = computed(() => {
  if (!partida.value) return 'Carregando...'; // Evita erro antes do onMounted
  const tempGame = new Chess(boardFen.value); // Usa a posição atual para o status
  if (tempGame.isCheckmate()) return 'Xeque-mate!';
  if (tempGame.isDraw()) return 'Empate!';
  return `Vez de: ${tempGame.turn() === 'w' ? 'Brancas' : 'Pretas'}`;
});

const currentEval = computed(() => {
  if (!partida.value || !partida.value.analyzedMoves || activeMoveIndex.value < 0) {
    return 0;
  }
  return partida.value.analyzedMoves[activeMoveIndex.value].evalAfter;
});

// --- CICLO DE VIDA ---
onMounted(async () => {
  const dadosPartida = await fetchGameById(route.params.id);
  partida.value = dadosPartida;

  const initialFen = dadosPartida.fenInicial || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  boardFen.value = initialFen;
});

// --- FUNÇÕES (MANIPULADORES DE EVENTOS) ---
function handleMove(move) {
  const tempGame = new Chess(boardFen.value);
  const result = tempGame.move(move);
  if (result) {
    boardFen.value = tempGame.fen();
  }
}

function resetGame() {
  const initialFen = partida.value?.fenInicial || 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  boardFen.value = initialFen;
  activeMoveIndex.value = -1;
}

function goToMove(index) {
  activeMoveIndex.value = index;

  const tempGame = new Chess();
  if (partida.value.fenInicial) {
    tempGame.load(partida.value.fenInicial);
  }

  for (let i = 0; i <= index; i++) {
    tempGame.move(partida.value.analyzedMoves[i].san);
  }
  boardFen.value = tempGame.fen();
}

function handleNavigate(direction) {
  if (!partida.value) return;
  const lastIndex = partida.value.analyzedMoves.length - 1;
  let newIndex = activeMoveIndex.value;

  if (direction === 'next') newIndex++;
  if (direction === 'prev') newIndex--;
  if (direction === 'first') newIndex = -1;
  if (direction === 'last') newIndex = lastIndex;

  if (newIndex >= -1 && newIndex <= lastIndex) {
    if (newIndex === -1) {
      resetGame();
    } else {
      goToMove(newIndex);
    }
  }
}
</script>

<style>
.game-layout { display: flex; gap: 2rem; }
.main-column { display: flex; flex-direction: column; gap: 1rem; }
</style>