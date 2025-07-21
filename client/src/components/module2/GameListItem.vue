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
  padding: 1.5rem; /* Aumenta o padding para mais respiro */
  background-color: var(--cor-superficie);
  border: 1px solid #2a222c;
  border-radius: var(--raio-borda);
  margin-bottom: 1rem; /* Espaçamento entre os itens */
  box-shadow: var(--sombra-suave);
  transition: transform 0.2s, box-shadow 0.2s;
}

.game-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.info {
  display: flex;
  flex-direction: column;
}

.nome {
  font-weight: 600; /* Um pouco mais de peso */
  font-size: 1.2rem;
  color: var(--cor-texto-principal);
}

.data {
  font-size: 0.95rem;
  color: var(--cor-texto-secundario);
}

.actions button {
  margin-left: 10px;
}

.actions button:first-child {
  background-color: #0accac;
  color: rgb(250, 248, 247);
}

.actions button:first-child:hover {
  background-color: var(--cor-primaria-hover);
}

.delete-btn {
  background-color: #e94747;
  color: white;
}

.delete-btn:hover {
  background-color: var(--cor-perigo-hover);
}
</style>