<script setup>
import { ref, onMounted, computed, watchEffect } from 'vue'; // 1. Adicione watchEffect
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
// ... outras importações ...
import TheChessboard from '../components/module4/ChessboardDisplay.vue';
import GameInfo from '../components/module4/GameInfo.vue';
import MoveHistory from '../components/module4/MoveHistory.vue';
import GameControls from '../components/module4/GameControls.vue';
import { fetchGameById } from '@/services/apiService';
import EvaluationBar from '@/components/module4/EvaluationBar.vue';

// --- ESTADO ---
const route = useRoute();
const router = useRouter();
const partida = ref(null);
const activeMoveIndex = ref(-1);
const boardAPI = ref(null); // A referência para a API do tabuleiro
const isPgnLoaded = ref(false);


const boardConfig = {
  movable: { // Só movimentos legais 
    free: false,
  },
  coordinates: true,
};

// Espera que o pgn seja carregado para comunicar com a API
watchEffect(() => {
  const pgn = partida.value?.pgn;
  const api = boardAPI.value;

  // Indica se o pgn foi carregado com sucesso 
  if (pgn && api && !isPgnLoaded.value) {
    console.log("✅ Condições satisfeitas! Carregando PGN...");
    console.log("PGN a ser carregado:", pgn);
    api.loadPgn(pgn);

    isPgnLoaded.value = true;
  }
});


// --- CICLO DE VIDA ---
onMounted(async () => {
  // Busca os dados da partida 
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
// Permite que va para uma move especifica 
function goToMove(index) {
    boardAPI.value?.viewHistory(index + 1);
    activeMoveIndex.value = index;
}
// Volta para o comeco do jogo
function resetGame() {
    boardAPI.value?.viewStart();
    activeMoveIndex.value = -1;
}
function handleBoardMove(move) {
    activeMoveIndex.value = boardAPI.value.getCurrentPlyNumber() - 1;
}

function goBack() { // Volta p/ a pagina anterior
  router.push('/partidas');
}
</script>

<template>
  <div v-if="!partida" class="loading-container">
    <p>Carregando análise da partida...</p>
  </div>
  <div v-else class="page-container">
    <div class="header">
      <button class="returnMenu" @click="goBack"> Retornar</button>
      <GameInfo :nome="partida.nome" :status="gameStatus" />
    </div>
    <div class="main-layout">
      <div class="board-block">
        <div class="board-area">
          <TheChessboard 
            :board-config="boardConfig"
            @board-created="(api) => boardAPI = api" 
            @move="handleBoardMove"
          />
          <EvaluationBar :evaluation="currentEval" />
        </div>
        <GameControls @reset="resetGame" @navigate="handleNavigate" />
      </div>

      <div class="sidebar-area">
        <MoveHistory 
      :analyzedMoves="partida.analyzedMoves"
      :currentEvaluation="currentEval"
      :activeMoveIndex="activeMoveIndex"
      @select-move="goToMove"
      />
      </div>

    </div>
  </div>
</template>

<style scoped>
.body{
  background-color: rgb(161, 117, 58);
}

.page-container {
  border: 3px solid #A772A7;
  background-color: #312433;
  padding-right: 3rem;
  padding-left: 3rem;
  padding-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center; 
  gap: 1rem;
}

.main-layout {
  display: flex; 
  flex-direction: row; 
  justify-content: center;
  gap: 2rem;
  width: 100%;
}

.board-block {
  display:flex;
  flex-direction: column;
  gap: 1rem;

}

.board-area {
  display: flex;
  flex-direction: row;
  
}

.sidebar-area {
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.header {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  width: 100%;
  position: relative;
}

.returnMenu {
  font-size: 1.3rem;
  position: absolute;
  left: 0.1rem;
  margin-right: 20px;
  border: 3px solid #A772A7;
  color: #A1E0B6;
  background-color: #312433;
}
.returnMenu:hover {
  background-color: #462b4b;
}
</style>
