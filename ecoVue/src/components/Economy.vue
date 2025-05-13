<template>
<div class="economy">
    <!-- 标题 -->
    <div class="ecoListHead"> 
        Leaderboard 
    </div>
    <div class="ecoList">
        <EcoTable />
    </div>
</div>
</template>
  
<script setup>
    import EcoTable from './EcoTable.vue'
    import EcoElTable from './EcoElTable.vue'
</script>
  
<style scoped>
    .economy {
        padding: 20px;
        width: 95%;
        margin: 0 auto;
        height: 100%; /* 确保父容器有高度 */
    }
    .ecoListHead {
        font-size: 24pt;
        font-weight: 500;
        color: black;
        margin-bottom: 15px;
        padding-left: 20px;
    }

    .ecoList {
        padding: 20px;
        width: 100%;
        margin: 0 auto;
        color: white;
        height: 100%; /* 确保父容器有高度 */
        display: flex;
        flex-direction: column; /* 启用弹性布局 */
    }
</style>