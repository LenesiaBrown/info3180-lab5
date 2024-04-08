<template>    
    <div class="movie_form">
        <h1>Add New Movie</h1>
        <div v-if="success">{{ success }}</div>
        <div v-if="errors">{{ errors }}</div>
        <form id="movieForm" @submit.prevent="saveMovie">        
            <div class="form-group">
                <label for="title" class="form-label">Movie Title</label>
                <input v-model="title" type="text" id="title" class="form-control"/>
            </div>
            <div class="form-group">
                <label for="description" class="form-label">Summary</label>
                <textarea v-model="description" id="description" class="form-control"></textarea>
            </div>
            <div class="form-group">
                <label for="poster" class="form-label">Poster</label>
                <br>
                <input type="file" @change="onFileChange" id="poster" class="form-control-file"/>
            </div>
            <button type="submit" class="button-add-movie">Submit</button>
        </form>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue';
let csrf_token = ref("");

const success = ref('');
const errors = ref('');
const title = ref('');
const description = ref('');
let posterFile = null;

function getCsrfToken() {
    return fetch('/api/v1/csrf-token')
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            // csrf_token.value = data.csrf_token;
            return data.csrf_token;
        });
}

onMounted(() => {
    getCsrfToken().then((token) => {
        csrf_token.value = token;
    });
});

const saveMovie = () => {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
        .then(function (response) {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to save movie');
            }
        })
        .then(function (data) {     
            success.value = data.message;   
            errors.value = '';    
            // console.log(data);
        })
        .catch(function (error) {
            success.value = '';
            errors.value = error.message;
            // console.log(error);
        });
    };

const onFileChange = (event) => {
    const files = event.target.files;
    if (files.length > 0) {
        posterFile = files[0];
    }
};



// onMounted(() => {
//     getCsrfToken();
// });
</script>


<style scoped>
.button-add-movie {
    background-color: #007bff;
    color: white; 
    padding: 8px 10px; 
    border: none;
    border-radius: 5px; 
    cursor: pointer; 
    margin-top: 20px;
}

.button-add-movie:hover {
    background-color: #0056b3;
}

.movie_form {
    margin-left: 30px;
}
</style>