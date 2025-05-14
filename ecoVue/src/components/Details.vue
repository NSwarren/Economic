<template>
<ImageShow />
</template>
  
<script setup>
    import ImageShow from './ImageShow.vue'
    import EcoElTable from './EcoElTable.vue'
</script>
  
<style scoped>
    .economy {
        padding-top: 20px;
        width: 100%;
        margin: 20px auto;
        
        height: 100%; /* 确保父容器有高度 */
        display: flex;
        flex-direction: column; /* 启用弹性布局 */
    }
</style>