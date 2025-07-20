<template>
  <div class="analysis-panel">
    <div class="eval-bar-container">
      <div class="eval-bar-white" :style="{ height: whiteHeight }"></div>
      <div class="eval-bar-black" :style="{ height: blackHeight }"></div>
      <div class="eval-text">{{ formattedEval }}</div>
    </div>

    <div class="move-history-container">
      <h2>Movimentos</h2>
      <ol class="move-list">
        <li v-for="(turn, turnIndex) in formattedTurns" :key="turnIndex" class="turn">
          <span class="turn-number">{{ turnIndex + 1 }}.</span>
          <span
            v-if="turn.white"
            :class="['move', `move-${turn.white.classification}`, { 'active-move': turn.white.moveIndex === activeMoveIndex }]"
            @click="emit('select-move', turn.white.moveIndex)"
          >
            {{ turn.white.san }}
          </span>
          <span
            v-if="turn.black"
            :class="['move', `move-${turn.black.classification}`, { 'active-move': turn.black.moveIndex === activeMoveIndex }]"
            @click="emit('select-move', turn.black.moveIndex)"
          >
            {{ turn.black.san }}
          </span>
        </li>
      </ol>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // Recebe a lista completa de movimentos analisados
  analyzedMoves: {
    type: Array,
    required: true,
    default: () => []
  },
  // Recebe a avaliação da posição ATUAL em centipawns
  currentEvaluation: {
    type: Number,
    default: 0
  },
  // Recebe o índice do lance que está sendo exibido no tabuleiro
  activeMoveIndex: {
    type: Number,
    default: -1
  }
});

const emit = defineEmits(['select-move']);

// Formata os movimentos em pares (Brancas/Pretas) para exibição
const formattedTurns = computed(() => {
  const turns = [];
  for (let i = 0; i < props.analyzedMoves.length; i += 2) {
    turns.push({
      white: { ...props.analyzedMoves[i], moveIndex: i },
      black: props.analyzedMoves[i + 1] ? { ...props.analyzedMoves[i + 1], moveIndex: i + 1 } : null
    });
  }
  return turns;
});

// Lógica da Barra de Avaliação
const maxEval = 500; // Define um teto de 5.0 (+5.00) para a barra não ficar extrema
const formattedEval = computed(() => (props.currentEvaluation / 100).toFixed(2));

const whiteHeight = computed(() => {
  const advantage = Math.max(0, props.currentEvaluation);
  const percentage = (Math.min(advantage, maxEval) / maxEval) * 50;
  return `${50 + percentage}%`;
});

const blackHeight = computed(() => {
  const advantage = Math.max(0, -props.currentEvaluation);
  const percentage = (Math.min(advantage, maxEval) / maxEval) * 50;
  return `${50 + percentage}%`;
});
</script>

<style scoped>
.analysis-panel {
  display: flex;
  flex-direction: column;
  width: 280px;
  background-color: #f8f9fa;
  border-left: 1px solid #dee2e6;
}

/* Barra de Avaliação */
.eval-bar-container {
  position: relative;
  width: 20px;
  height: 400px; /* Altura da barra */
  background-color: #495057;
  display: none; /* Descomente se quiser a barra ao lado */
}
/* ... estilos para .eval-bar-white, .eval-bar-black, .eval-text ... */

/* Lista de Movimentos */
.move-history-container {
  padding: 15px;
  overflow-y: auto;
  height: 100%;
}

.move-list {
  list-style: none;
  padding: 0;
  font-family: 'Courier New', Courier, monospace;
}

.turn {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.turn-number {
  width: 30px;
  color: #6c757d;
}

.move {
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 8px;
  transition: background-color 0.2s;
}

.active-move {
  background-color: #cfe2ff;
  border: 1px solid #9ec5fe;
}

/* Cores da Classificação dos Lances */
.move-best { color: #198754; font-weight: bold; }
.move-good { color: #212529; }
.move-inaccuracy { color: #ffc107; }
.move-mistake { color: #fd7e14; }
.move-blunder { color: #dc3545; font-weight: bold; }
</style>