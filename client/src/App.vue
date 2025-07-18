<script setup>
import ChessReview from './components/ChessReview.vue';
</script>

<template>
  <main>
    <h1>Análise de Partida de Xadrez</h1>
    <ChessReview />
  </main>
</template>

<style>
/* Estilos globais básicos */
body {
  font-family: sans-serif;
  background-color: #f0f0f0;
  color: #333;
}
main {
  max-width: 900px;
  margin: 2rem auto;
  padding: 1rem;
}
h1 {
  text-align: center;
}
</style>