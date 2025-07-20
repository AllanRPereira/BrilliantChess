<template>
  <div class="game-view-container">
    <div class="game-layout">
      <div class="main-column">
        <GameInfo :nome="partida.nome" :status="gameStatus" />
        <ChessboardDisplay :fen="boardFen" @move="handleMove" />
        <GameControls @reset="resetGame" />
      </div>
      <MoveHistory :history="gameHistory" />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { Chess } from 'chess.js';
import { fetchGameById } from '../services/apiService.js';

// Importando os novos componentes
import GameInfo from '../components/module4/GameInfo.vue';
import ChessboardDisplay from '../components/module4/ChessboardDisplay.vue';
import MoveHistory from '../components/module4/MoveHistory.vue';
import GameControls from '../components/module4/GameControls.vue';
// --- LÓGICA DE ESTADO (continua no pai) ---
const route = useRoute();
const game = reactive(new Chess());
const partida = ref({});
const boardFen = ref('');
// ... lógica de carregamento e erro ...

onMounted(async () => {
  // ... busca os dados da partida e carrega o 'game' e 'boardFen' ...
});

// --- DADOS COMPUTADOS PARA OS FILHOS ---
const gameHistory = computed(() => game.history({ verbose: true }));
const gameStatus = computed(() => {
  if (game.isCheckmate()) return 'Xeque-mate!';
  if (game.isDraw()) return 'Empate!';
  return `Vez de: ${game.turn() === 'w' ? 'Brancas' : 'Pretas'}`;
});

// --- MANIPULADORES DE EVENTOS VINDOS DOS FILHOS ---
function handleMove(move) {
  const result = game.move(move);
  if (result) {
    boardFen.value = game.fen(); // Atualiza o FEN, que será passado para o filho
  }
}

function resetGame() {
  game.load(partida.value.fenInicial);
  boardFen.value = game.fen();
}
</script>

<style>
/* Estilos principais da página */
.game-layout { display: flex; gap: 2rem; }
.main-column { display: flex; flex-direction: column; gap: 1rem; }
</style>