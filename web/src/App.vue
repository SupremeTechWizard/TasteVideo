<script setup lang="ts">
import {ref, onMounted, onUnmounted} from 'vue';
import {useUserStore} from './stores/userStore';
import LoginForm from './components/LoginForm.vue';
import RegisterForm from './components/RegisterForm.vue';
import VideoPlayer from './components/VideoPlayer.vue';
import VideoUploadForm from "./components/VideoUploadForm.vue";

const videos = ref([]);
const currentVideo = ref(null);
const currentVideoIndex = ref(0);
const userStore = useUserStore();

const switchVideo = (event) => {
  if (event.key === 'ArrowUp' && currentVideoIndex.value > 0) {
    currentVideoIndex.value--;
    currentVideo.value = videos.value[currentVideoIndex.value];
  } else if (event.key === 'ArrowDown' && currentVideoIndex.value < videos.value.length - 1) {
    currentVideoIndex.value++;
    currentVideo.value = videos.value[currentVideoIndex.value];
  }
};

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

const isUploadModalVisible = ref(false);

const showUploadModal = () => {
  isUploadModalVisible.value = true;
};

const hideUploadModal = () => {
  isUploadModalVisible.value = false;
};

const fetchVideosByCategory = async (category) => {
  try {
    const response = await fetch(`http://localhost:8000/GetVideosByCategory?category=${category}`);
    if (response.ok) {
      videos.value = await response.json();
      currentVideoIndex.value = 0;
      currentVideo.value = videos.value[currentVideoIndex.value];
    } else {
      console.error('获取分类视频列表失败:', response.statusText);
    }
  } catch (error) {
    console.error('获取分类视频时发生错误:', error);
  }
};
</script>

<template>
  <div class="flex flex-col h-screen w-screen">
    <nav class="flex justify-between p-2.5 bg-gray-900 text-white">
      <div>
        <button @click="fetchVideosByCategory('热门视频')"
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
          热门视频
        </button>
        <button @click="fetchVideosByCategory('体育频道')"
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
          体育频道
        </button>
        <button @click="fetchVideosByCategory('旅游')"
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
          旅游
        </button>
        <button @click="fetchVideosByCategory('音乐')"
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
          音乐
        </button>
      </div>
      <div>
        <button v-if="userStore.state.isLoggedIn" @click="showUploadModal"
                class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
          上传视频
        </button>
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
      </div>
    </nav>
    <VideoPlayer class="overflow-hidden" :videoSrc="currentVideo.src" v-if="currentVideo"/>
    <LoginForm v-if="isLoginModalVisible" @close="hideLoginModal" @login-success="handleLoginSuccess"/>
    <RegisterForm v-if="isRegisterModalVisible" @close="hideRegisterModal"/> <!-- 注册表单 -->
    <VideoUploadForm v-if="isUploadModalVisible" @close="hideUploadModal"/>
  </div>
</template>
