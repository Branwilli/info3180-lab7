<template>
    <div class="movies-view">
      <h1>Movie Listings</h1>
  
      <div v-if="movies.length === 0">
        <p>No movies available.</p>
      </div>
  
      <div v-else class="movie-list">
      <div v-for="movie in movies" :key="movie.id" class="movie-card">
        <img
          v-if="movie.poster"
          :src="`/uploads/${movie.poster}`"
          :alt="movie.title"
          class="poster"
        />
        <div class="movie-info">
          <h2>{{ movie.title }}</h2>
          <p>{{ movie.description }}</p>
        </div>
      </div>
      </div>
    </div>
  </template>

<script setup>
import { ref, onMounted } from 'vue';

const movies = ref([]);

function fetchMovies() {
  fetch('/api/v1/movies') 
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); 
    })
    .then(data => {
      movies.value = data; 
    })
    .catch(error => {
      console.error('Error fetching movies:', error); 
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<style scoped>
.movies-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.movie-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.movie-card {
  display: flex;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.poster {
  width: 180px;
  height: 100%;
  object-fit: cover;
}

.movie-info {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.movie-info h2 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.movie-info p {
  font-size: 0.95rem;
  color: #555;
}

.no-movies {
  text-align: center;
  font-style: italic;
}
</style>