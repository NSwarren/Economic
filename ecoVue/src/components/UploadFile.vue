<template>
  <div class="modal-mask" @click.self="handleMaskClick">
  <div class="modal-wrapper">
  <div class="uploadDiv">
    <!-- 文件选择区域 -->
    <div class="upload-area" @dragover.prevent @drop="handleDrop">
      <input
          type="file"
          ref="fileInput"
          @change="handleFileSelect"
          multiple
          hidden
        />
      <button @click="triggerFileSelect">Flies Select</button>
      <p>drag and drop files to this area</p>
      <p v-if="files.length">Selected: {{ files.length }} 个</p>
    </div>
  
      <!-- 文件列表预览 -->
      <div v-if="files.length" class="file-list">
        <div v-for="(file, index) in files" :key="index" class="file-item">
          <div class="file-info">
            <span>{{ file.name }}</span>
          </div>
          <div class="progress-container">
            <span>{{ formatSize(file.size) }}</span>
          </div>
          <button @click="removeFile(index)">Remove</button>
        </div>
      </div>
  
      <!-- 上传控制 -->
      <div class="controls">
        <!-- <input type="file" @change="handleFileChange" ref="fileInput" multiple />
        <button @click="uploadFiles">上传文件</button> -->

        <button @click="uploadFiles" :disabled="uploading">
          {{ uploading ? 'Uploading...' : 'Start' }}
        </button>
        <button @click="reset">Reset</button>
      </div>
  
      <!-- 状态提示 -->
      <div v-if="message" :class="['message', message.type]">
        {{ message.text }}
      </div>
  </div>
  </div>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import api from '@/services/api'

  const fileSize = 10 * 1024 * 1024
  const fileType = ['image/jpeg', 'image/png', 'application/pdf']

  const emit = defineEmits(['close', 'upload-success'])
  const files = ref([]);
  const uploading = ref(false);
  const message = ref(null);
  const fileInput = ref(null);

   // 文件选择
   const triggerFileSelect = () => {
    fileInput.value.click();
  };
  
  // 处理文件选择
  const handleFileSelect = (e) => {
    addFiles([...e.target.files]);
    e.target.value = ''; 
  };

  // 处理拖放文件
  const handleDrop = (e) => {
    e.preventDefault();
    addFiles([...e.dataTransfer.files]);
  };

  // 新增弹窗控制逻辑
  const closeModal = () => {
    reset()
    emit('close')
  }
  // 添加文件到列表
  const addFiles = (newFiles) => {
    const validFiles = newFiles.filter(file => {
      if (file.size > fileSize) { // 限制10MB
        showMessage(`File ${file.name} : Size limit exceeded`, 'error');
        return false;
      }
      if (!fileType.includes(file.type)) {
        showMessage(`File ${file.name}  : Type unsupported`, 'error');
        return false;
      }
      return true;
    });
    files.value = [
      ...files.value.filter(existingFile => 
        !validFiles.some(newFile => newFile.name === existingFile.name) // 过滤掉重复文件
      ),
      ...validFiles.map(file => ({
        file,
        name: file.name,
        size: file.size,
        progress: 0
      }))
  ];
  };
  
  // 移除文件
  const removeFile = (index) => {
    files.value.splice(index, 1);
  };
  
  // 格式化文件大小
  const formatSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };
  
  // 显示消息提示
  const showMessage = (text, type = 'info') => {
    message.value = { text, type };
    setTimeout(() => message.value = null, 3000);
  };

  const uploadFiles = async () => {
    if (files.value.length === 0) {
      showMessage('Please select a file first', 'error');
      return;
    }

    const formData = new FormData();
    files.value.forEach((items) => {
      formData.append('files', items.file);
    });

    if (formData.getAll('files').length === 0) {
      showMessage('Please select a file first', 'error');
      // console.error('FormData 为空，请选择文件');
      return;
    }

    try {
      const result = await api.uploadFiles(formData);
      if (result) {
        showMessage('File uploaded successfully', 'success');
        reset();
      } else {
        showMessage('File uploaded failed', 'error')
      }
    } catch (error) {
      showMessage('File uploaded failed', 'error')
    }
  };
  // 重置状态
  const reset = () => {
    files.value = [];
  };

  const handleMaskClick = (event) => {
    closeModal()
  }

</script>
  
<style scoped>
  /* 弹窗样式 */
  .modal-mask {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    transition: opacity 0.3s ease;
    cursor: pointer;
  }
  .modal-wrapper {
    max-width: 90%;
    width: 600px;
    cursor: auto;
  }
  .uploadDiv {
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
    transition: all 0.3s ease;
    
    max-width: 600px;
    margin: 2rem auto;
    padding: 1rem;
    border: 1px solid #eee;
  }
  
  .upload-area {
    border: 2px dashed #ccc;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1rem;
  }
  
  .file-list {
    font-size: small;
    margin: 1rem 0;
    height: 100px;
    overflow-y: auto;
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none;  /* IE/Edge */
  }
  
  .file-item {
    display: flex;
    align-items: center;
    padding: 0.5rem;
    border-bottom: 1px solid #eee;
  }
  
  .file-info {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  .progress-container {
    width: 200px;
    height: 20px;
    border-radius: 4px;
    margin: 0 1rem;
    position: relative;
  }
  .controls {
    margin-top: 1rem;
    text-align: center;
  }
  
  button {
    padding: 0.5rem 1rem;
    margin: 0 0.5rem;
    background: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:disabled {
    background: #ccc;
    cursor: not-allowed;
  }
  
  .message {
    font-size: small;
    padding: 0.5rem;
    margin-top: 1rem;
    border-radius: 4px;
  }
  
  .message.success {
    background: #dff0d8;
    color: #3c763d;
  }
  
  .message.error {
    background: #f2dede;
    color: #a94442;
  }
</style>
