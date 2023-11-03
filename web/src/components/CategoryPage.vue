<template>
  <div>
    <h2>视频分类</h2>
    <ul>
      <li v-for="category in categories" :key="category">
        <a href="#" @click="fetchVideosByCategory(category)">{{ category }}</a>
      </li>
    </ul>
    <div v-if="selectedVideos.length">
      <VideoPlayer v-for="video in selectedVideos" :key="video.id" :videoSrc="video.src" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import VideoPlayer from './VideoPlayer.vue';

const categories = ref(['热门视频', '体育频道', '旅游', '音乐']);
const selectedVideos = ref([]);

const fetchVideosByCategory = async (category) => {
  const response = await fetch(`http://localhost:8000/SearchVideos?query=${category}`);
  selectedVideos.value = await response.json();
};
</script>
