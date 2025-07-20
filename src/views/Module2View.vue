<script setup>
import { ref, onMounted } from 'vue';
import { fetchGames } from '../services/apiService.js';
import GameList from '../components/module2/GmeList.vue';
import{ deleteGame } from '../services/apiService.js; //importa a função deletar
import { computed } from 'vue'; // Importe o 'computed' para a reatividade.
import { useRouter } from 'vue-router'; // Importe o router para a navegação.
import SearchBar from '../components/module2/SearchBar.vue';


//armazena os dados e o estado da interface
const partidas = ref([]); // Armazena a lista de partidas vinda da API.
const carregando = ref(true); // Indica se estamos esperando a resposta da API.
const erro = ref(null); // Armazena mensagens de erro, se houver.
const router = useRouter();
const termoBusca = ref('');

// A função onMounted é um gancho do Vue que executa o código
onMounted(async () => {
  try {
    // Chama nossa função de API simulada para buscar os dados.
    const dadosRecebidos = await fetchGames();
    partidas.value = dadosRecebidos;
  } catch (e) {
    // Em caso de erro na API, aparece a mensagem
    erro.value = 'Falha ao carregar as partidas. Tente novamente mais tarde.';
    console.error(e);
  } finally {
    //o carregamento termina.
    carregando.value = false;
  }
});


// função para lida com a exclusão
const handleApagar = async (partidaId) => {
  // Pede confirmação do usuário antes de deletar
  if (!confirm('Tem certeza que deseja apagar esta análise? A ação não pode ser desfeita.')) {
    return;
  }
  
  try {
    // Chama a função da API simulada para deletar.
    await deleteGame(partidaId);
    partidas.value = partidas.value.filter(p => p.id !== partidaId);
  } catch (error) {
    // Em caso de erro, avisa
    alert('Erro ao apagar a partida. Tente novamente.');
    console.error(error);
  }
};


// --- LÓGICA ---
// ... onMounted

//a função recalcula seu valor automaticamente sempre que uma dependencia muda
const partidasFiltradas = computed(() => {
  // Se a busca estiver vazia, retorna a lista completa
  if (!termoBusca.value) {
    return partidas.value;
  }
  // Se não, filtra a lista de partidas
  return partidas.value.filter(partida =>
    // Converte ambos os textos para minúsculas
    partida.nome.toLowerCase().includes(termoBusca.value.toLowerCase())
  );
});

// ... handleApagar

// Atualiza a função para usar o router.
const handleVerAnalise = (partidaId) => {
  console.log(`Navegando para /partidas/${partidaId}`);
  // Usa o router para navegar para a página de detalhes da partida.
  router.push(`/partidas/${partidaId}`);
};



</script>

<template>
  <div class="module-container">
    <h1>Minhas Análises de Partidas</h1>
    
    <div v-if="carregando" class="feedback-container">
      <p>Carregando partidas...</p>
    </div>
    
    <div v-else-if="erro" class="error-message">
      <p>{{ erro }}</p>
    </div>

    <div v-else class="content-container">
      <p>Conteúdo do Módulo 2 aparecerá aqui.</p>
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
  background-color: #ffdddd;
  border: 1px solid red;
  padding: 10px;
  border-radius: 5px;
}
.feedback-container {
  text-align: center;
  padding: 20px;
  color: #666;
}
</style>

</script>

<GameList 
  :partidas="partidas"
  @apagar="handleApagar"
  @ver-analise="handleVerAnalise"
/>

</script>

<div v-else class="content-container">
  <SearchBar v-model="termoBusca" />

  <GameList 
    :partidas="partidasFiltradas" @apagar="handleApagar"
    @ver-analise="handleVerAnalise"
  />
</div>