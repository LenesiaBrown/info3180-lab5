<template>
    <h1>Movies</h1>
    <div>    
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="movie in movies" :key="movie.id" class="movie-list">
        <img :src="movie.poster" alt="Movie Poster" class="movie-poster">
        <h3>{{ movie.title }}</h3>
        <p>{{ movie.description }}</p>        
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);
let loading = ref(true);

onMounted(() => {
  fetchMovies();
});

const fetchMovies = async () => {
  try {
    const response = await fetch('/api/v1/movies');
    if (response.ok) {
      const data = await response.json();
      movies.value = data.movies;
    } else {
      console.error('Failed to fetch movies');
    }
  } catch (error) {
    console.error('Error fetching movies:', error);
  } finally {
    loading.value = false;
  }
};
</script>