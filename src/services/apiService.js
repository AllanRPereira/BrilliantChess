//simula a comunicação com a API
//lista de partidas em memória que independe do backend.
import { ref } from 'vue';

//dados exemplos, na implementação virão de um banco de dados.
const mockGames = ref([
  { id: 1, nome: 'Vitória Clássica vs. Magnus', data: '2025-07-18' },
  { id: 2, nome: 'Abertura Siciliana Fulminante', data: '2025-07-17' },
  { id: 3, nome: 'Defesa Francesa - Partida de Estudo', data: '2025-07-16' },
  { id: 4, nome: 'Gambito da Dama Recusado', data: '2025-07-15' },
]);

// Simula a busca de todas as partidas
export const fetchGames = () => {
  return new Promise((resolve) => {
    // Simula um atraso de 1 segundo , carregando
    setTimeout(() => {
      console.log('API Mock: Buscando partidas...');
      resolve([...mockGames.value]); // Retorna uma cópia dos dados.
    }, 1000);
  });
};

// Simula a exclusão de uma partida por ID
export const deleteGame = (gameId) => {
  return new Promise((resolve, reject) => {
    // Simula um atraso de 500ms da rede.
    setTimeout(() => {
      const initialLength = mockGames.value.length;
      mockGames.value = mockGames.value.filter(game => game.id !== gameId);
      
      // Verifica se algum item foi realmente removido e finaliza a busca
      if (mockGames.value.length < initialLength) {
        console.log(`API Mock: Partida com ID ${gameId} deletada.`);
        resolve({ success: true, message: 'Partida deletada com sucesso.' });
      } else {
        console.error(`API Mock: Partida com ID ${gameId} não encontrada.`);
        reject(new Error('Partida não encontrada para exclusão.'));
      }
    }, 500);
  });
};