<script setup>
import { ref, onMounted, computed } from 'vue';
import { Chessboard } from 'vue-chessboard';
import 'vue-chessboard/dist/style.css';
import { Chess } from 'chess.js';

// --- 1. ESTADO E REFERÊNCIAS ---

const chess = new Chess(); // Instância da lógica do xadrez
const boardAPI = ref(null); // API do componente vue-chessboard
const boardConfig = ref({
  fen: 'start', // Posição inicial
  viewOnly: true, // Apenas visualização
});

// PGN de uma partida famosa (A Partida da Ópera - Paul Morphy)
const pgn = `
[Event "A Night at the Opera"]
[Site "Paris, France"]
[Date "1858"]
[White "Paul Morphy"]
[Black "Duke Karl / Count Isouard"]
[Result "1-0"]

1. e4 e5 2. Nf3 d6 3. d4 Bg4 4. dxe5 Bxf3 5. Qxf3 dxe5 6. Bc4 Nf6 7. Qb3 Qe7
8. Nc3 c6 9. Bg5 b5 10. Nxb5 cxb5 11. Bxb5+ Nbd7 12. O-O-O Rd8 13. Rxd7 Rxd7
14. Rd1 Qe6 15. Bxd7+ Nxd7 16. Qb8+ Nxb8 17. Rd8# 1-0
`;

const gameHistory = ref([]);
const currentMoveIndex = ref(-1); // -1 representa a posição inicial

// --- 2. LÓGICA DO JOGO ---

onMounted(() => {
  loadPgn();
});

function loadPgn() {
  chess.loadPgn(pgn);
  gameHistory.value = chess.history({ verbose: true });
  chess.reset(); // Volta para a posição inicial após carregar
  updateBoard();
}

// Atualiza o FEN (notação da posição) para o tabuleiro
function updateBoard() {
  boardConfig.value.fen = chess.fen();
}

// --- 3. MÉTODOS DE NAVEGAÇÃO ---

function goToStart() {
  chess.reset();
  currentMoveIndex.value = -1;
  updateBoard();
}

function goBack() {
  if (currentMoveIndex.value >= 0) {
    chess.undo();
    currentMoveIndex.value--;
    updateBoard();
  }
}

function goForward() {
  if (currentMoveIndex.value < gameHistory.value.length - 1) {
    currentMoveIndex.value++;
    chess.move(gameHistory.value[currentMoveIndex.value].san);
    updateBoard();
  }
}

function goToEnd() {
  chess.loadPgn(pgn); // Maneira mais fácil de ir para o final
  currentMoveIndex.value = gameHistory.value.length - 1;
  updateBoard();
}

// --- 4. PROPRIEDADES COMPUTADAS (para desabilitar botões) ---

const isAtStart = computed(() => currentMoveIndex.value < 0);
const isAtEnd = computed(() => currentMoveIndex.value === gameHistory.value.length - 1);

</script>

<template>
  <div class="review-container">
    <div class="board-wrapper">
      <Chessboard :board-config="boardConfig" @board-created="(api) => (boardAPI = api)" />
    </div>

    <div class="controls-panel">
      <h3>Lances da Partida</h3>
      <div class="move-list">
        <ol>
          <li v-for="(move, index) in gameHistory" :key="index">
            <span v-if="index % 2 === 0">{{ Math.floor(index / 2) + 1 }}.</span>
            <span :class="{ 'current-move': index === currentMoveIndex }">
              {{ move.san }}
            </span>
          </li>
        </ol>
      </div>

      <div class="navigation-controls">
        <button @click="goToStart" :disabled="isAtStart">|&lt;</button>
        <button @click="goBack" :disabled="isAtStart">&lt;</button>
        <button @click="goForward" :disabled="isAtEnd">&gt;</button>
        <button @click="goToEnd" :disabled="isAtEnd">&gt;|</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.review-container {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  justify-content: center;
}

.board-wrapper {
  flex-basis: 512px; /* Tamanho padrão do tabuleiro */
  max-width: 100%;
}

.controls-panel {
  flex-basis: 300px;
  display: flex;
  flex-direction: column;
}

.move-list {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 1rem;
  height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.move-list ol {
  list-style: none;
  padding: 0;
  margin: 0;
}

.move-list li {
  display: inline-block;
  margin-right: 0.75rem;
  padding: 4px;
  border-radius: 4px;
  font-size: 1rem;
}

.move-list .current-move {
  background-color: #ffc107; /* Amarelo para destacar */
  font-weight: bold;
}

.navigation-controls {
  display: flex;
  justify-content: space-around;
}

.navigation-controls button {
  font-size: 1.5rem;
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background-color: #e9e9e9;
  cursor: pointer;
}

.navigation-controls button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.navigation-controls button:hover:not(:disabled) {
  background-color: #dcdcdc;
}
</style>