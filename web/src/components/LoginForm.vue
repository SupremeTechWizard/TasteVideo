<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-600 bg-opacity-50" @click="handleOutsideClick">
    <div class="bg-white p-5 rounded-lg shadow-lg w-full max-w-md mx-auto" ref="modalContent">
      <h2 class="text-xl mb-4">登录</h2>
      <input type="email" v-model="email" placeholder="邮箱" class="border p-2 w-full mb-4" required>
      <input type="password" v-model="password" placeholder="密码" class="border p-2 w-full mb-4" required>
      <button @click="login" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full">
        登录
      </button>
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import {onMounted, onUnmounted, ref} from 'vue';
import {useUserStore} from '../stores/userStore';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const modalContent = ref(null);

const userStore = useUserStore();

const emit = defineEmits(['close', 'login-success'])

const handleOutsideClick = (event) => {
  if (modalContent.value && !modalContent.value.contains(event.target)) {
    closeModal();
  }
};
const closeModal = () => {
  emit('close');
};

onMounted(() => {
  window.addEventListener('click', handleOutsideClick);
});

onUnmounted(() => {
  window.removeEventListener('click', handleOutsideClick);
});

const login = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch('http://localhost:8000/Login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email.value,
        password: password.value
      })
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      userStore.setUser(data.user);
      userStore.setLoggedIn(true);
      emit('login-success', data.user);
      closeModal();
    } else {
      throw new Error('登录失败！');
    }
  } catch (error) {
    errorMessage.value = '登录失败，请检查你的邮箱和密码！';
    console.error('登录出错：', error);
  }
};
</script>
