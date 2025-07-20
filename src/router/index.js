import { createRouter, createWebHistory } from 'vue-router';
import Module2View from '../views/Module2View.vue'; 

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
      component: { template: '<div><h1>Detalhes da Partida ID: {{$route.params.id}}</h1><router-link to="/partidas">Voltar</router-link></div>' }
    }
  ]
});

export default router;