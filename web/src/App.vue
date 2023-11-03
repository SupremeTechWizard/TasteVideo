<script setup lang="ts">
import {ref, onMounted, onUnmounted} from 'vue';
import {useUserStore} from './stores/userStore';
import LoginForm from './components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import VideoPlayer from './components/VideoPlayer.vue';

const videos = ref([]);
const currentVideo = ref(null);
const currentVideoIndex = ref(0);
const userStore = useUserStore();

const switchVideo = (event) => {
  if (event.key === 'ArrowUp' && currentVideoIndex.value > 0) {
    currentVideoIndex.value--;
  } else if (event.key === 'ArrowDown' && currentVideoIndex.value < videos.value.length - 1) {
    currentVideoIndex.value++;
  }
  currentVideo.value = videos.value[currentVideoIndex.value];
}

const logout = () => {
  userStore.setToken(null);
  userStore.setUser(null);
  userStore.setLoggedIn(false);
};

onMounted(async () => {
  const response = await fetch('http://localhost:8000/GetVideos');
  if (response.ok) {
    videos.value = await response.json();
    currentVideo.value = videos.value[0];
  } else {
    console.error('获取视频列表失败:', response.statusText);
  }
  window.addEventListener('keydown', switchVideo);
  await userStore.checkAuth();
});

onUnmounted(() => {
  window.removeEventListener('keydown', switchVideo);
});

const isLoginModalVisible = ref(false);

const showLoginModal = () => {
  isLoginModalVisible.value = true;
};

const hideLoginModal = () => {
  isLoginModalVisible.value = false;
};

const handleLoginSuccess = (userData) => {
  hideLoginModal();
  console.log('用户登录成功：', userData);
};

const isRegisterModalVisible = ref(false);

const showRegisterModal = () => {
  isRegisterModalVisible.value = true;
};

const hideRegisterModal = () => {
  isRegisterModalVisible.value = false;
};
</script>

<template>
  <div class="app-container">
    <nav class="flex justify-end p-2.5 bg-gray-900 text-white">
      <button
          v-if="!userStore.state.isLoggedIn"
          @click.stop="showLoginModal"
          class="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75"
      >
        登录
      </button>
      <button
          v-if="!userStore.state.isLoggedIn"
          @click="showRegisterModal"
          class="px-4 py-2 ml-2 bg-green-500 text-white font-semibold rounded-lg shadow-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-75"
      >
        注册
      </button>
      <button
          v-if="userStore.state.isLoggedIn"
          @click="logout"
          class="px-4 py-2 bg-red-500 text-white font-semibold rounded-lg shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-75"
      >
        注销
      </button>
    </nav>
    <VideoPlayer :videoSrc="currentVideo.src" v-if="currentVideo"/>
    <LoginForm v-if="isLoginModalVisible" @close="hideLoginModal" @login-success="handleLoginSuccess"/>
    <RegisterForm v-if="isRegisterModalVisible" @close="hideRegisterModal"/> <!-- 注册表单 -->
  </div>
</template>
