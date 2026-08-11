<template>
  <div class="page-container">
    <h1>页面二</h1>
    <p>这是第二个页面</p>
    <div class="button-group">
      <button @click="goToPageOne" class="nav-button">前往页面一</button>
      <button @click="goToHomePage" class="nav-button">前往主页面</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToPageOne = () => {
  router.push('/');
};

const goToHomePage = () => {
  router.push('/home');
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #e8f4fd;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

p {
  margin-bottom: 30px;
  color: #666;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.nav-button {
  padding: 10px 20px;
  margin: 0 10px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.nav-button:hover {
  background-color: #0b7dda;
}
</style>
