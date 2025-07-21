<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app-layout">
    <header class="app-header">
      <h2>BrilliantChess</h2>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
#app-layout {
  background-color: #382F3A;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: #382f3a;
  padding: 1rem 2rem;
  border-bottom: 5px solid #a772a7;
  box-shadow: var(--sombra-suave);
}

.app-header h2 {
  margin: 0;
  color: rgb(161, 224, 182);
}

main {
  flex-grow: 1; /* Faz o conteúdo principal ocupar o espaço disponível */
  padding: 2rem;
}
</style>