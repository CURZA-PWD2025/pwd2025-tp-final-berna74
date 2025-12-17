<template>
    <div class="container">
      <h2>Detalle de la categoría</h2>
      <h3>Nombre : {{ categoria.nombre }}</h3>
      <h4>ID: {{ categoria.id }}</h4>
  
      <RouterLink :to="{ name: 'categorias_list' }"><button>Volver</button> </RouterLink>
    </div>
  </template>
  
  <script setup lang="ts">
  import { toRefs, onMounted } from 'vue'
  import useCategoriaStore from '../../stores/categorias'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const { categoria, categorias } = toRefs(useCategoriaStore())
  
  onMounted(() => {
    const id = route.params.id
    console.log(id)
    categoria.value = categorias.value.find((categoria) => categoria.id == parseInt(id as string)) ?? {
      nombre: '',
    }
  })
</script>
<style scoped>
.container {
  max-width: 700px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>