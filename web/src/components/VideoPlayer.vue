<template>
  <div class="video-container">
    <video ref="videoElement" controls autoplay :src="videoSrc" @play="onPlay" @pause="onPause"
           @loadedmetadata="autoPlayVideo">
      Your browser does not support the video tag.
    </video>
  </div>
</template>

<script setup lang="ts">
import {ref, watch} from 'vue';

const props = defineProps<{
  videoSrc: string;
}>();

const videoElement = ref<HTMLVideoElement | null>(null);

watch(
    () => props.videoSrc,
    (newSrc, oldSrc) => {
      if (videoElement.value && newSrc !== oldSrc) {
        videoElement.value.load();
        autoPlayVideo();
      }
    },
    {immediate: true}
);

const autoPlayVideo = () => {
  if (videoElement.value) {
    setTimeout(() => {
      videoElement.value?.play();
    }, 0);
  }
};

const onPlay = () => {
  console.log('Video is playing');
};

const onPause = () => {
  console.log('Video is paused');
};
</script>

<style scoped>
.video-container {
  top: 0;
  left: 0;
  width: 100vw;
  height: calc(100vh - 60px);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
