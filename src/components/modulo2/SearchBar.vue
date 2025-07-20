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
  width: 100%;
  padding: 12px;
  font-size: 1em;
  margin-bottom: 20px;
  box-sizing: border-box; /* Garante que padding não afete a largura total */
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style>