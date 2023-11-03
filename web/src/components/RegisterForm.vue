<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gray-600 bg-opacity-50" @click="handleOutsideClick">
    <div class="bg-white p-5 rounded-lg shadow-lg w-full max-w-md mx-auto" ref="modalContent">
      <h2 class="text-xl mb-4">注册</h2>
      <form @submit.prevent="register">
        <input type="email" v-model="email" placeholder="邮箱" class="border p-2 w-full mb-4" required>
        <input type="password" v-model="password" placeholder="密码" class="border p-2 w-full mb-4" required>
        <button type="submit" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded w-full">
          注册
        </button>
        <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useUserStore} from '../stores/userStore';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const modalContent = ref(null);

const userStore = useUserStore();

const emit = defineEmits(['close'])

const handleOutsideClick = (event) => {
  if (modalContent.value && !modalContent.value.contains(event.target)) {
    closeModal();
  }
};

const closeModal = () => {
  emit('close');
};

const register = async () => {
  errorMessage.value = '';
  try {
    const response = await fetch('http://localhost:8000/CreateUser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({email: email.value, password: password.value}),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      userStore.setToken(data.access_token);
      userStore.setUser({email: data.email, id: data.id});
      userStore.setLoggedIn(true);
      closeModal();
      console.log('注册成功！');
    } else {
      throw new Error('注册失败！');
    }
  } catch (error) {
    errorMessage.value = '注册失败，请检查你的邮箱和密码是否正确！';
    console.error('注册出错：', error);
  }
};
</script>
