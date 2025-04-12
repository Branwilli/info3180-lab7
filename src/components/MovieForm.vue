<script setup>
import { ref, onMounted } from 'vue';

const movie = ref({
    title: '',
    description: '',
});

const posterFile = ref('');
const successMessage = ref('');

function handleFileUpload(event) {
  posterFile.value = event.target.files[0];
}

function saveMovie() {
  const form_data = new FormData();
  form_data.append('title', movie.value.title);
  form_data.append('description', movie.value.description);
  form_data.append('poster', posterFile.value);

  fetch('/api/v1/movies', {
    method: 'POST',
    body: form_data,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log(data);
      successMessage.value = data.message || 'Movie added!';
    })
    .catch(error => {
      console.error('Error:', error);
    });
};

const csrf_token = ref('');

function getCsrfToken(){
    fetch('/api/v1/csrf-token') 
        .then((response) => response.json()) 
        .then((data) => { 
            console.log(data); 
            csrf_token.value = data.csrf_token; 
    }) 
};

onMounted(() => {
    getCsrfToken();
});
</script>

<template>
    <div class="form-container">
        <h2>Add a Movie</h2>
            <form @submit.prevent="saveMovie" id="movieForm" enctype="multipart/form-data">
              <div class="form-group mb-3">
                    <label for="title">Title:</label>
                    <input type="text" id="title" class="form-control" v-model="movie.title"/>
                </div>

                <div class="form-group mb-3">
                    <label for="description">Description:</label>
                    <textarea id="description" class="form-control" v-model="movie.description"></textarea>
                </div>

                <div class="form-group mb-3">
                    <label for="poster">Upload Poster:</label>
                    <input type="file" id="poster" @change="handleFileUpload" class="form-control"/>
                </div>
                
                <button type="submit">Submit</button>
            </form>

        <p v-if="successMessage" class="success">{{ successMessage }}</p> 
  </div>
</template>

<style scoped>
.form-container {
  max-width: 500px;
  margin: auto;
  padding: 1rem;
  border-radius: 10px;
  background: #f0f0f0;
}
input,
textarea {
  display: block;
  width: 100%;
  margin-bottom: 1rem;
  padding: 0.5rem;
}
button {
  padding: 0.6rem 1.2rem;
}
.success {
  margin-top: 1rem;
  color: green;
}
</style>