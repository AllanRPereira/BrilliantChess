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
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background-color: var(--cor-superficie);
  padding: 1rem 2rem;
  border-bottom: 1px solid var(--cor-borda);
  box-shadow: var(--sombra-suave);
}

.app-header h2 {
  margin: 0;
  color: var(--cor-primaria);
}

main {
  flex-grow: 1; /* Faz o conteúdo principal ocupar o espaço disponível */
  padding: 2rem;
}
</style>