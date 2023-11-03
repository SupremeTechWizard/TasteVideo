<template>
  <form @submit.prevent="register">
    <div>
      <label for="email">邮箱:</label>
      <input id="email" v-model="email" type="email" required>
    </div>
    <div>
      <label for="password">密码:</label>
      <input id="password" v-model="password" type="password" required>
    </div>
    <button type="submit">注册</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const email = ref('');
const password = ref('');

const register = async () => {
  const response = await fetch('http://localhost:8000/CreateUser', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email: email.value, password: password.value }),
  });

  if (response.ok) {
    console.log('注册成功！');
  } else {
    console.error('注册失败！');
  }
};
</script>
