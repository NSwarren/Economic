<template>
<div class="economy">
    <!-- 标题 -->
    <div class="economytHead"> 
        Leaderboard 
    </div>
    <ImageShow />
</div>
</template>
  
<script setup>
    import ImageShow from './ImageShow.vue'
    import EcoElTable from './EcoElTable.vue'
</script>
  
<style scoped>
    .economy {
        padding-top: 20px;
        width: 90%;
        margin: 20px auto;
        
        height: 100%; /* 确保父容器有高度 */
        display: flex;
        flex-direction: column; /* 启用弹性布局 */
    }
    .economytHead {
        background-color: #1A3F90;
        font-size: 24pt;
        font-weight: 500;
        color: black;
        margin: 0 20px;
        width : 100%;
        height: 120px;
    }
</style>