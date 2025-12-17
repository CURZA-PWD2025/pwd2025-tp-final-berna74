<template>
    <div class="container">
    <h2>Categorías</h2>
    <router-link :to="{name: 'categorias_create'}"><button>Crear Categoría</button></router-link>
    
    <div v-if="categorias.length === 0" class="alert alert-info mt-3">
      No hay categorías registradas. Haz clic en "Crear Categoría" para agregar una.
    </div>

    <table v-else class="table table-striped mt-3">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="categoria in categorias" :key="categoria.id">
          <td>{{ categoria.id }}</td>
          <td>{{ categoria.nombre }}</td>
          <td class="actions">
           <router-link v-if="categoria.id" :to="{name: 'categorias_show', params: {id: categoria.id }}">
             <button class="btn-icon" title="Ver">
               <Icon icon="mdi:eye" width="18" height="18" />
             </button>
           </router-link>
           <router-link v-if="categoria.id" :to="{name: 'categorias_edit', params: {id: categoria.id }}">
             <button class="btn-icon" title="Editar">
               <Icon icon="mdi:pencil" width="18" height="18" />
             </button>
           </router-link>
           <button @click.prevent="eliminar(categoria.id as number)" class="btn-icon btn-delete" title="Eliminar">
             <Icon icon="mdi:delete" width="18" height="18" />
           </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </template>
  
  <script setup lang="ts">
  import { onMounted } from 'vue';
  import { toRefs } from 'vue';
  import { Icon } from '@iconify/vue';
  import useCategoriaStore from '@/stores/categorias';
  
  const {categorias} = toRefs(useCategoriaStore());
  const { getAll, destroy } = useCategoriaStore();
  
  onMounted(async() => {
    await getAll();
  });
  
  async function eliminar (id: number) {
    if (confirm('¿Estás seguro de eliminar la categoría ' + id + '?')) {
      if (confirm('Esta acción no se puede deshacer. ¿Deseas continuar?')) {
        console.log('Eliminando categoría con ID:', id);
        try {
          await destroy(id);
          await getAll();
          console.log('Categoría eliminada exitosamente');
        } catch (error) {
          console.error('Error al eliminar categoría:', error);
          alert('Error al eliminar la categoría. Puede estar asociada a otros registros.');
        }
      } else {
        console.log('Eliminación cancelada por el usuario.');
      }
    }
  }
  
  </script>
  
  <style scoped>
   .container {
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  }

  h2 {
    margin-bottom: 1.5rem;
  }

  button {
    margin-bottom: 1.5rem;
  }
  
  .actions {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
  }
  
  .btn-icon {
    background: none;
    border: none;
    padding: 0.5rem;
    cursor: pointer;
    color: #022F9D;
    border-radius: 4px;
    transition: all 0.3s ease;
  }
  
  .btn-icon:hover {
    background: #e3f0fc;
    color: #00CDFF;
  }
  
  .btn-delete:hover {
    background: #ffebee;
    color: #c62828;
  }
  </style>