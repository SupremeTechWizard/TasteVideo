<template>
  <div class="video-container">
    <video ref="videoElement" controls autoplay :src="videoSrc" @play="onPlay" @pause="onPause"
           @loadedmetadata="autoPlayVideo" class="w-full h-full">
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