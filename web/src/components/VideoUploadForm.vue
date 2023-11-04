<template>
  <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center" @click="handleOutsideClick">
    <div class="bg-white p-5 rounded-lg shadow-lg w-full max-w-md mx-auto">
      <input type="file" @change="handleFileChange" accept="video/*" class="mb-4"/>
      <button @click="uploadVideo"
              class="px-4 py-2 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75">
        上传视频
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useUserStore} from '../stores/userStore';

const selectedFile = ref(null);
const userStore = useUserStore();

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadVideo = async () => {
  if (selectedFile.value) {
    const formData = new FormData();
    formData.append('file', selectedFile.value);

    try {
      const response = await fetch('http://localhost:8000/UploadVideo', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${userStore.state.token}`
        },
        body: formData
      });

      if (response.ok) {
        console.log('视频上传成功！');
      } else {
        console.error('视频上传失败！');
      }
    } catch (error) {
      console.error('上传过程中出现错误：', error);
    }
  }
};

const emit = defineEmits(['close']);

const handleOutsideClick = (event) => {
  if (event.target === event.currentTarget) {
    emit('close');
  }
};
</script>
