<template>
  <div class="analysis-panel">
    <div class="move-history-container">
      <h2>Movimentos</h2>
      <ol class="move-list">
        <li v-for="(turn, turnIndex) in formattedTurns" :key="turnIndex" class="turn">
          <span class="turn-number">{{ turnIndex + 1 }}.</span>
          <span
            v-if="turn.white"
            :class="['move', `move-${turn.white.classification}`, { 'active-move': turn.white.moveIndex === activeMoveIndex }]"
            @click="selectMove(turn.white.moveIndex)"
          >
            {{ turn.white.san }}
          </span>
          <span
            v-if="turn.black"
            :class="['move', `move-${turn.black.classification}`, { 'active-move': turn.black.moveIndex === activeMoveIndex }]"
            @click="selectMove(turn.black.moveIndex)"
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

// As props 'currentEvaluation' não é mais necessária aqui
const props = defineProps({
  analyzedMoves: { type: Array, required: true },
  activeMoveIndex: { type: Number, default: -1 }
});

const emit = defineEmits(['select-move']);

// A lógica da barra foi removida. Apenas a formatação dos lances permanece.
const formattedTurns = computed(() => {
  const turns = [];
  if (!props.analyzedMoves) return [];
  for (let i = 0; i < props.analyzedMoves.length; i += 2) {
    turns.push({
      white: { ...props.analyzedMoves[i], moveIndex: i },
      black: props.analyzedMoves[i + 1] ? { ...props.analyzedMoves[i + 1], moveIndex: i + 1 } : null
    });
  }
  return turns;
});

function selectMove(index) {
  emit('select-move', index);
}
</script>

<style scoped>
/* O CSS da barra de avaliação foi removido */
.analysis-panel {
  width: 350px;
  height: 500px;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 5px;
}
/* Estilos da lista de lances (move-history-container, move-list, etc) permanecem */
.move-history-container {
  padding: 10px 15px;
  overflow-y: auto;
  height: 100%;
}
/* ... etc ... */
</style>