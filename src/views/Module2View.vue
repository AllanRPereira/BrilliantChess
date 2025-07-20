<script setup>
import { ref, onMounted } from 'vue';
import { fetchGames } from '../services/apiService.js';

//armazena os dados e o estado da interface.
const partidas = ref([]); // Armazena a lista de partidas vinda da API.
const carregando = ref(true); // Indica se estamos esperando a resposta da API.
const erro = ref(null); // Armazena mensagens de erro, se houver.

// A função onMounted é executada automaticamente quando o componente é criado.
onMounted(async () => {
  try {
    // Chama nossa função de API
    const dadosRecebidos = await fetchGames();
    partidas.value = dadosRecebidos;
  } catch (e) {
    // Em caso de erro na "API", aparece a mensagem.
    erro.value = 'Falha ao carregar as partidas. Tente novamente mais tarde.';
    console.error(e);
  } finally {
    // termina o carregamento
    carregando.value = false;
  }
});

// o template mostra o carregamento ou erro.
</script>

<template>
  <div class="module-container">
    <h1>Minhas Análises de Partidas</h1>
    
    <div v-if="carregando">
      <p>Carregando partidas...</p>
    </div>
    
    <div v-else-if="erro" class="error-message">
      <p>{{ erro }}</p>
    </div>

    <div v-else>
      </div>
  </div>
</template>

<style scoped>
.module-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
  font-family: sans-serif;
}
.error-message {
  color: red;
}
</style>