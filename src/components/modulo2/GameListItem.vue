<script setup>
// Define as propriedades que este componente recebe do componente pai (GameList).
// Isso garante que cada item da lista saiba qual partida exibir.
defineProps({
  partida: {
    type: Object, // Espera um objeto.
    required: true, // É obrigatório.
  },
});

// Define os eventos que este componente pode emitir para o pai.
// Quando um botão é clicado, o componente "avisa" o pai sobre a ação.
const emit = defineEmits(['ver-analise', 'apagar']);
</script>

<template>
  <li class="game-item">
    <div class="info">
      <span class="nome">{{ partida.nome }}</span>
      <span class="data">Data: {{ new Date(partida.data).toLocaleDateString() }}</span>
    </div>
    <div class="actions">
      <button @click="emit('ver-analise', partida.id)">Ver Análise</button>
      <button @click="emit('apagar', partida.id)" class="delete-btn">Apagar</button>
    </div>
  </li>
</template>

<style scoped>
.game-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}
.game-item:hover {
  background-color: #f9f9f9;
}
.info {
  display: flex;
  flex-direction: column;
}
.nome {
  font-weight: bold;
  font-size: 1.1em;
}
.data {
  font-size: 0.9em;
  color: #666;
}
.actions button {
  margin-left: 10px;
  padding: 8px 12px;
  border-radius: 5px;
  border: 1px solid #ccc;
  cursor: pointer;
}
.delete-btn {
  background-color: #e74c3c;
  color: white;
  border-color: #c0392b;
}
.delete-btn:hover {
  background-color: #c0392b;
}
</style>