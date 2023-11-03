<script setup lang="ts">
import {ref, onMounted, onUnmounted} from 'vue';
import VideoPlayer from './components/VideoPlayer.vue';

const videos = ref([]);
const currentVideo = ref(null);
const currentVideoIndex = ref(0);

const switchVideo = (event) => {
  if (event.key === 'ArrowUp' && currentVideoIndex.value > 0) {
    currentVideoIndex.value--;
  } else if (event.key === 'ArrowDown' && currentVideoIndex.value < videos.value.length - 1) {
    currentVideoIndex.value++;
  }
  currentVideo.value = videos.value[currentVideoIndex.value];
}

onMounted(async () => {
  const response = await fetch('http://localhost:8000/GetVideos');
  if (response.ok) {
    videos.value = await response.json();
    currentVideo.value = videos.value[0];
  } else {
    console.error('获取视频列表失败:', response.statusText);
  }
  window.addEventListener('keydown', switchVideo);
});

onUnmounted(() => {
  window.removeEventListener('keydown', switchVideo);
});
</script>

<template>
  <VideoPlayer :videoSrc="currentVideo.src" v-if="currentVideo"/>
</template>
