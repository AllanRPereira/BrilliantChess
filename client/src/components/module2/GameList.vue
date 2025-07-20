<script setup>
import GameListItem from './GameListItem.vue';

// Recebe a lista de partidas que devem ser exibidas.
defineProps({
  partidas: {
    type: Array,
    required: true,
  },
});

// Repassa os eventos do filho (GameListItem) para o componente "avô" (Module2View),
// permitindo que a lógica principal seja centralizada na view.
const emit = defineEmits(['ver-analise', 'apagar']);
</script>

<template>
  <ul class="game-list" v-if="partidas.length > 0">
    <GameListItem
      v-for="partida in partidas"
      :key="partida.id"
      :partida="partida"
      @ver-analise="emit('ver-analise', partida.id)"
      @apagar="emit('apagar', partida.id)"
    />
  </ul>
  <p v-else class="feedback-container">Nenhuma partida encontrada.</p>
</template>

<style scoped>
.game-list {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}
</style>