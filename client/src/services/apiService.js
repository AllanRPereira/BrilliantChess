//simula a comunicação com a API
//lista de partidas em memória que independe do backend.
import { ref } from 'vue';
import { DADOS_ANALISADOS_MOCK } from './mockData';

//dados exemplos, na implementação virão de um banco de dados.
const mockGames = ref([
  { id: 1, nome: 'Vitória do allan vs Magnus Carlsen', data: '2025-07-18' },
  { id: 2, nome: 'Gambito secreto máximo', data: '2025-07-17' },
  { id: 3, nome: 'Foschiera lindo', data: '2025-07-16' },
  { id: 4, nome: 'partida exemplo 4', data: '2025-07-15' },
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

export const fetchGameById = (id) => {
  /*return new Promise((resolve, reject) => {
    // Simula uma chamada de rede
    setTimeout(() => {
      // Encontra a partida pelo ID no seu array de dados simulados
      // Supondo que você tenha uma constante DADOS_SIMULADOS em algum lugar
      const partida = DADOS_SIMULADOS.find(p => p.id == id);

      if (partida) {
        // Se a partida for encontrada, retorna seus dados.
        // É uma boa prática adicionar o PGN ou FEN aqui se não estiver presente.
        if (!partida.pgn) {
          partida.pgn = '1. e4 e5 2. Nf3 Nc6'; // Exemplo de PGN
        }
        resolve(partida);
      } else {
        // Se nenhuma partida for encontrada com esse ID, rejeita a promessa.
        reject(new Error(`Partida com ID ${id} não encontrada.`));
      }
    }, 500); // Simula um atraso de 500ms
  }); */
  return Promise.resolve(DADOS_ANALISADOS_MOCK)
};

// ... (suposição de onde seus dados estão)
// Este array deve existir no seu arquivo para que a função acima funcione.
const DADOS_SIMULADOS = [
    { id: 1, nome: 'Análise Rápida: Defesa Siciliana', pgn: '1. e4 c5' },
    { id: 2, nome: 'Estudo de Finais: Carlsen vs. Nepo', pgn: '1. d4 Nf6' },
    // ... outras partidas
];

