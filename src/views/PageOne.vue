<template>
  <div class="page-container">
    <h1>页面一</h1>
    <p>这是第一个页面</p>
    <div class="button-group">
      <button @click="goToPageTwo" class="nav-button">前往页面二</button>
      <button @click="goToHomePage" class="nav-button">前往主页面</button>
    </div>
    <div class="input-container">
      <input 
        type="text" 
        v-model="inputText" 
        placeholder="请输入内容..." 
        class="text-input"
        @keyup.enter="handleSendData"
      />
      <button @click="handleSendData" class="send-button">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { sendVueData } from '../services/api'

const router = useRouter();
const inputText = ref('');

const goToPageTwo = () => {
  router.push('/page-two');
};

const goToHomePage = () => {
  router.push('/home');
};

const handleSendData = async () => {
  try {
    const response = await sendVueData(String(inputText.value)); // 确保转换为字符串
    console.log('后端返回:', response.data);
  } catch (error) {
    console.error('发送失败:', error);
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
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
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.nav-button:hover {
  background-color: #45a049;
}

.input-container {
  display: flex;
  align-items: center;
  margin-top: 30px;
  width: 80%;
  max-width: 500px;
}

.text-input {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
  outline: none;
  transition: border-color 0.3s;
}

.text-input:focus {
  border-color: #4CAF50;
}

.send-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  padding: 0 15px;
  height: 46px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-button:hover {
  background-color: #45a049;
}
</style>
