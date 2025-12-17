<template>
  <div class="profesores-list">
    <div class="header">
      <h2>Lista de Profesores</h2>
      <button @click="showCreateForm = true" class="btn-primary">
        <Icon icon="mdi:plus" width="20" height="20" />
        Nuevo Profesor
      </button>
    </div>

    <ProfesoresCreate v-if="showCreateForm" @close="showCreateForm = false" @created="handleCreated" />

    <div v-if="loading" class="loading">Cargando profesores...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="profesores-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Horarios de clases</th>
            <th>Teléfono</th>
            <th>Email</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="profesor in profesores" :key="profesor.id">
            <td>{{ profesor.id }}</td>
            <td>{{ profesor.nombre }}</td>
            <td>{{ profesor.apellido }}</td>
            <td>{{ profesor.horarios_clases }}</td>
            <td>{{ profesor.telefono }}</td>
            <td>{{ profesor.email }}</td>
            <td class="actions">
              <button @click="viewProfesor(profesor.id)" class="btn-icon" title="Ver">
                <Icon icon="mdi:eye" width="18" height="18" />
              </button>
              <button @click="editProfesor(profesor.id)" class="btn-icon" title="Editar">
                <Icon icon="mdi:pencil" width="18" height="18" />
              </button>
              <button @click="confirmDelete(profesor.id)" class="btn-icon btn-delete" title="Eliminar">
                <Icon icon="mdi:delete" width="18" height="18" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ProfesoresShow v-if="showingProfesorId" :id="showingProfesorId" @close="showingProfesorId = null" />
    <ProfesoresUpdate v-if="editingProfesorId" :id="editingProfesorId" @close="editingProfesorId = null" @updated="handleUpdated" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import { useProfesoresStore } from '@/stores/profesores'
import { storeToRefs } from 'pinia'
import ProfesoresCreate from './ProfesoresCreate.vue'
import ProfesoresShow from './ProfesoresShow.vue'
import ProfesoresUpdate from './ProfesoresUpdate.vue'

const profesoresStore = useProfesoresStore()
const { profesores, loading, error } = storeToRefs(profesoresStore)

const showCreateForm = ref(false)
const showingProfesorId = ref<number | null>(null)
const editingProfesorId = ref<number | null>(null)

onMounted(() => {
  profesoresStore.fetchProfesores()
})

function viewProfesor(id: number) {
  showingProfesorId.value = id
}

function editProfesor(id: number) {
  editingProfesorId.value = id
}

function confirmDelete(id: number) {
  if (confirm('¿Está seguro de que desea eliminar este profesor?')) {
    profesoresStore.deleteProfesor(id)
  }
}

function handleCreated() {
  showCreateForm.value = false
  profesoresStore.fetchProfesores()
}

function handleUpdated() {
  editingProfesorId.value = null
  profesoresStore.fetchProfesores()
}
</script>

<style scoped>
.profesores-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.profesores-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.profesores-table th,
.profesores-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

.profesores-table th {
  background-color: #022F9D;
  color: #FFFFFF;
}

.profesores-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.btn-primary {
  background: #00CDFF;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: #00B8E6;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 205, 255, 0.3);
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

.loading,
.error {
  padding: 20px;
  text-align: center;
}

.error {
  color: #f44336;
}
</style>
