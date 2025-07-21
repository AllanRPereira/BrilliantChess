<template>
  <div class="eval-bar-container">
    <div class="eval-bar-white" :style="{ height: whiteHeight }"></div>
    <div class="eval-text">{{ formattedEval }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  // A avaliação é o único dado que este componente precisa
  evaluation: {
    type: Number,
    default: 0
  }
});

// A lógica é a mesma que tínhamos antes
const formattedEval = computed(() => {
  const pawnAdvantage = props.evaluation / 100;
  return (pawnAdvantage > 0 ? '+' : '') + pawnAdvantage.toFixed(2);
});

const whiteHeight = computed(() => {
  const maxEval = 1000; // Vantagem de 10 peões
  const clampedEval = Math.max(-maxEval, Math.min(maxEval, props.evaluation));
  const percentage = 50 + (clampedEval / maxEval) * 50;
  return `${percentage}%`;
});
</script>

<style scoped>
.eval-bar-container {
  position: relative;
  width: 30px;
  height: 100%; /* Ocupa a altura do container pai */
  background-color: #403D39;
  border-radius: 4px;
  overflow: hidden; /* Garante que a barra interna não ultrapasse a borda arredondada */
  transition: all 0.3s ease;
}

.eval-bar-white {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: #f8f9fa;
  transition: height 0.3s ease-in-out;
}

.eval-text {
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  color: #a94442;
  font-weight: bold;
  font-size: 12px;
  mix-blend-mode: difference;
}
</style>