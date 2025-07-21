<script setup>
import { ref, onMounted, computed, watchEffect } from 'vue'; // 1. Adicione watchEffect
import { useRoute } from 'vue-router';
// ... outras importações ...
import TheChessboard from '../components/module4/ChessboardDisplay.vue';
import GameInfo from '../components/module4/GameInfo.vue';
import MoveHistory from '../components/module4/MoveHistory.vue';
import GameControls from '../components/module4/GameControls.vue';
import { fetchGameById } from '@/services/apiService';

// --- ESTADO ---
const route = useRoute();
const partida = ref(null);
const activeMoveIndex = ref(-1);
const boardAPI = ref(null); // A referência para a API do tabuleiro
const isPgnLoaded = ref(false);

// 2. Simplifique o boardConfig. Ele não precisa mais do evento 'create'.
const boardConfig = {
  movable: {
    free: false,
  },
  coordinates: true,
};

// 3. O "Vigia" Inteligente: watchEffect
// Este bloco de código vai rodar automaticamente quando 'partida' E 'boardAPI' tiverem valores.
watchEffect(() => {
  const pgn = partida.value?.pgn;
  const api = boardAPI.value;

  // Só executa se ambas as condições forem verdadeiras
  if (pgn && api && !isPgnLoaded.value) {
    console.log("✅ Condições satisfeitas! Carregando PGN...");
    console.log("PGN a ser carregado:", pgn);
    api.loadPgn(pgn);

    isPgnLoaded.value = true;
  }
});


// --- CICLO DE VIDA ---
onMounted(async () => {
  // A única responsabilidade do onMounted agora é buscar os dados.
  partida.value = await fetchGameById(route.params.id);
});

// --- PROPRIEDADES COMPUTADAS ---
const gameStatus = computed(() => {
  if (!boardAPI.value) return 'Carregando...';
  if (boardAPI.value.getIsCheckmate()) return 'Xeque-mate!';
  if (boardAPI.value.getIsDraw()) return 'Empate!';
  return `Vez de: ${boardAPI.value.getTurnColor() === 'w' ? 'Brancas' : 'Pretas'}`;
});

const currentEval = computed(() => {
    if (!partida.value || activeMoveIndex.value < 0) return 0;
    return partida.value.analyzedMoves[activeMoveIndex.value].evalAfter;
});


// --- FUNÇÕES ---
function handleNavigate(direction) {
    if (!boardAPI.value) return;
    if (direction === 'next') boardAPI.value.viewNext();
    if (direction === 'prev') boardAPI.value.viewPrevious();
    if (direction === 'first') boardAPI.value.viewStart();
    if (direction === 'last') boardAPI.value.viewHistory(partida.value.analyzedMoves.length);
    activeMoveIndex.value = boardAPI.value.getCurrentPlyNumber() - 1;
}
// ... suas outras funções (goToMove, resetGame, handleBoardMove) ...
function goToMove(index) {
    boardAPI.value?.viewHistory(index + 1);
    activeMoveIndex.value = index;
}
function resetGame() {
    boardAPI.value?.viewStart();
    activeMoveIndex.value = -1;
}
function handleBoardMove(move) {
    activeMoveIndex.value = boardAPI.value.getCurrentPlyNumber() - 1;
}
</script>

<template>
  <div v-if="!partida" class="loading-container">
    <p>Carregando análise da partida...</p>
  </div>
  <div v-else class="game-view-container">
    <div class="game-layout">
      <div class="main-column">
        <GameInfo :nome="partida.nome" :status="gameStatus" />
        
        <TheChessboard 
          :board-config="boardConfig"
          @board-created="(api) => boardAPI = api" 
          @move="handleBoardMove"
        />
        
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

<style>
.game-layout { display: flex; gap: 2rem; }
.main-column { display: flex; flex-direction: column; gap: 1rem; }
</style>