<template>
<div class="economy">
    <!-- 标题 -->
    <div class="economytHead">
        <div class="top-header">
            <img src="../../public/Image/cuhk.png" class="logo">
        <div class="logo-title">
            Chinese University of Hong Kong <br>
            Department of <br>
            Computer Science and Engineering
        </div>

        <div class="logo-title2">
            ARTIFICIAL INTELLIGENCE <br>
            IN HEALTHCARE GROUP
        </div>

        <div class="logo-title-right">
            <div class="first">SCMBench</div>
            <div class="second"> Single Cell Multi-omics Integration Benchmark</div>
        </div>
        </div>
    </div>
    <router-view/>
</div>
</template>
  
<script setup>
    import EcoTable from './EcoTable.vue'
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
        /* font-size: 24pt;
        font-weight: 500; */
        margin: 0 20px;
        width: 100%;
    }
    .top-header{
        margin: 0 auto;
        padding: 20px 45px;
        clear: both;
        color: #c6daf0
    }

    .logo {
        display: inline-block;
        vertical-align: middle;
    }
    .logo-title, .logo-title2 {
        display: inline-block;
        vertical-align: middle;
        font-size: 18px;
        line-height: 1.2;
    }
    .logo-title {
        margin-left: 15px;
        padding-right: 10px;
    }
    .logo-title2 {
        padding-left: 15px;
        position: relative;
    }
    .logo-title2:before {
        content: "";
        display: block;
        width: 2px;
        height: 55px;
        background-color: #756b5c;
        position: absolute;
        left: 0;
        top: 4px;
    }
    .logo-title-right {
        float: right;
        text-align: right;
        font-weight: 1000;
        color: #f5f5f5;
    }
    .logo-title-right .first {
        font-size: 30px;
        font-family: Anton, sans-serif;
    }
    .logo-title-right.second {
        font-size: 14px;
        color: #c6daf0;
        font-family: Varela Round, sans-serif;
    }

</style>