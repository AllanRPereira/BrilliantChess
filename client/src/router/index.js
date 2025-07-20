import { createRouter, createWebHistory } from 'vue-router';
// Visualização da página inicil
import Module2View from '../views/Module2View.vue'; 
// Visualização da partida 
import Module4View from '../views/Module4View.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Rota para a página inicial
    {
      path: '/',
      redirect: '/partidas' // Redireciona a raiz para o módulo 2
    },
    // Rota principal do módulo 2
    {
      path: '/partidas',
      name: 'listaDePartidas',
      component: Module2View
    },
    // Rota de exemplo
    {
      path: '/partidas/:id',
      name: 'detalheDaPartida',
      // com se dá a navegação
      component: Module4View
    }
  ]
});

export default router;