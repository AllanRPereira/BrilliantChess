<script setup>
defineProps({
  modelValue: { type: String, default: '' },
});
const emit = defineEmits(['update:modelValue']);

// Função que emite o evento com o input
const onInput = (event) => {
  emit('update:modelValue', event.target.value);
};
</script>

<template>
  <div class="search-container">
    <input
      type="text"
      :value="modelValue"
      @input="onInput"
      placeholder="Buscar partida por nome..."
    />
  </div>
</template>

<style scoped>
.search-container input {
  background-color:#382F3A;
  color: #9DD8B0;
  width: 100%;
  padding: 12px 15px;
  font-size: 1.2rem;
  margin-bottom: 2rem; /* Aumenta o espaçamento inferior */
  box-sizing: border-box;
  border: 2px solid #2a222c;
  border-radius: var(--raio-borda);
  transition: border-color 0.2s, box-shadow 0.2s;
}

/* Efeito visual quando o usuário clica no campo de busca */
.search-container input:focus {
  outline: none;
  border-color: var(--cor-primaria);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}
</style>