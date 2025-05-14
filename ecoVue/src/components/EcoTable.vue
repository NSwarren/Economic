<template>
<div class="ecoList">
    <!-- 数据表格 -->
    <div class="ecoListTables" ref="tableContainer">
        <!-- 表头 -->
        <div class="ecoListTableHeadDiv">
            <table class="ecoListTableHead">
                <colgroup>
                    <col v-for="(col, index) in columnWidths" 
                        :key="index"
                        :style="{ width: col + 'px' }">
                    <col v-for="(col, index) in dynamicWidths" 
                        :key="index"
                        :style="{ width: col + 'px' }">
                </colgroup>
                <thead>
                    <tr>
                        <!-- Methods 和 Datasets -->
                        <!-- <th v-for="(header, index) in baseHeaders" :key ="index"
                            :rowspan="2">
                            <template v-if="header.key === 'datasets'">
                                <select v-model="dselectedType" class="type-filter">
                                    <option value="">Datasets</option>
                                    <option v-for="type in duniqueTypes" :key="type" :value="type">
                                        {{ type }}
                                    </option>
                                </select>
                            </template>
                            <template v-else>
                                {{ header.title }}
                            </template>
                        </th> -->
                        <th  >
                            <button class="submit-btn"
                             @click="showRatioModal = true">Score Cal</button>
                        </th>
                        <th  > </th>
                        <th :colspan="5">Integration Accuracy</th>
                        <th :colspan="5">Bio Conservation</th>
                        <th :colspan="5">Batch Correction</th>
                        <th v-if="showScoreColumn"
                            :rowspan = "2"
                            :class="{
                                'active':sortKey === 'score'
                            }"
                            
                            @click=" toggleSort('score')"
                            >
                            Score
                            <span class="sort-indicator">
                                {{ showSortIndicator('score') }}
                            </span>
                        </th>
                    </tr>
                    <tr>
                        <th v-for="(header, index) in baseHeaders" :key ="index"
                            :rowspan="2">
                            <template v-if="header.key === 'datasets'">
                                <select v-model="dselectedType" class="type-filter">
                                    <option value="">Datasets</option>
                                    <option v-for="type in duniqueTypes" :key="type" :value="type">
                                        {{ type }}
                                    </option>
                                </select>
                            </template>
                            <template v-else>
                                {{ header.title }}
                            </template>
                        </th>
                        <th v-for="(header, index) in tableHeaders" 
                            :key="index"
                            :class="{ 
                                'sortable': header.sortable,
                                'active': header.sortable && sortKey === header.key,
                                'resizable':index < tableHeaders.length - 1
                            }"
                            @click="header.sortable ? toggleSort(header.key) : null"
                            >
                            <div class="header-content">
                                <template v-if="header.key === 'datasets'">
                                    <!-- 保持下拉框 -->
                                </template>
                                <template v-else>
                                    {{ header.title }}
                                </template>
                                <span v-if="header.sortable" class="sort-indicator">
                                    {{ showSortIndicator(header.key) }}
                                </span>
                            </div>
                        </th>
                    </tr>
                </thead>
            </table>
        </div>
        
        <!-- 内容 -->
        <div  class="ecoListTableBodyDiv" @scroll="handleScroll">
            <table class="ecoListTableBody">
                <colgroup>
                    <col v-for="(col, index) in columnWidths" 
                        :key="index"
                        :style="{ width: col + 'px' }">
                    <col v-for="(col, index) in dynamicWidths" 
                        :key="index"
                        :style="{ width: col + 'px' }">
                </colgroup>
                <tbody>
                    <tr v-for="item in filteredData" :key="item.id">
                        <td v-for="(header, index) in baseHeaders" :key="index">
                            <template v-if="index === 0">
                                <template v-if="item.datasets === 'PBMC-10x'">
                                    <router-link 
                                        :to="{ name: 'ImageShow', params: { name: item.methods } }"
                                        class="detail-link">
                                        {{ item[header.key] }}
                                    </router-link>
                                </template>
                                <template v-else>
                                    {{ item[header.key] }}
                                </template>
                            </template>
                            <template v-else>
                                {{ item[header.key] }}
                            </template>
                        </td>
                        <td v-for="(header, index) in tableHeaders" :key="index">
                            {{ item[header.key] }}
                        </td>
                        <td 
                            v-if="showScoreColumn"
                            class="score-cell"
                            >
                            {{ item['score'] }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div v-if="showRatioModal" class="modalRatio">
    <div class="modal-content">
      <h3 class="modal-title">Score Calculate</h3>
      
      <!-- 自定义表单结构 -->
      <div class="custom-form">
        <div class="form-item">
          <label>Integration Accuracy</label>
          <input 
            type="number" 
            v-model.number="ratioForm.ia"
            min="0" 
            max="1" 
            step="0.1"
            @input="validateSum"
          >
        </div>
        
        <div class="form-item">
          <label>Bio Conservation</label>
          <input 
            type="number" 
            v-model.number="ratioForm.bio"
            min="0" 
            max="1" 
            step="0.1"
            @input="validateSum"
          >
        </div>
        
        <div class="form-item">
          <label>Batch Correction</label>
          <input 
            type="number" 
            v-model.number="ratioForm.batch"
            min="0" 
            max="1" 
            step="0.1"
            @input="validateSum"
          >
        </div>
        
        <div class="error-msg" v-if="errorMessage">
          {{ errorMessage }}
        </div>
        
        <div class="form-actions">
          <button class="cancel-btn" @click="showRatioModal = false">Cancel</button>
          <button 
            class="submit-btn" 
            @click="calculateOverall"
            :disabled="!!errorMessage"
          >Calculate</button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
  
<script setup>
    import { ref, computed, onMounted, watch, nextTick  } from 'vue'
    import api from '@/services/api'
    import UploadModal from './UploadFile.vue'

    const baseHeaders = [
        { title: 'Method', key: 'methods', sortable: false },
        { title: ' ', key: 'datasets', sortable: false }
    ]
    const metricHeaders = {
        'Integration Accuracy': [
            { title: 'Mean Average Precision' , key: 'mean_average_precision', sortable: true },
            { title: 'Normalized Mutual Info' , key: 'normalized_mutual_info', sortable: true },
            { title: 'Avg Silhouette Width' , key: 'avg_silhouette_width', sortable: true },
            { title: 'ARI' , key: 'ari', sortable: true },
            { title: 'overall' , key: 'ia_overall', sortable: true }
        ],
        'Bio Conservation':[
            { title: 'Traj Conserv' , key: 'traj_conserv', sortable: true },
            { title: 'Biomarker' , key: 'biomarker', sortable: true },
            { title: 'DARs', key: 'dars', sortable: true },
            { title: 'Enriched Motif' , key: 'enriched_motif', sortable: true },
            { title: 'Overall' , key: 'bio_overall', sortable: true }
        ],
        'Batch Correction' : [
            { title: 'Ilisi' , key: 'ilisi', sortable: true },
            { title: 'Kbet' , key: 'kbet', sortable: true },
            { title: 'Graph Connectivity' , key: 'graph_connectivity', sortable: true },
            { title: 'Avg Silhouette Width Batch' , key: 'avg_silhouette_width_batch', sortable: true },
            { title: 'Overall' , key: 'batch_overall', sortable: true }
        ]
    }
    const tableHeaders = computed(() => {
        return Object.values(metricHeaders).flat();
    });

    const rawData = ref([])

    const selectedType = ref('Integration Accuracy')

    // 根据选择筛选
    const dselectedType = ref('')
    const duniqueTypes = ref([''])
    const filteredData = computed(() => {
        return sortedData.value.filter(item => {
            // Type筛选条件
            const typeMatch = dselectedType.value ? 
            item.datasets === dselectedType.value : 
            true
            
            return typeMatch
        })
    })

    // 排序
    const sortKey = ref('id')
    const sortOrder = ref('asc')
    const showSortIndicator = (key) => {
        if (sortKey.value === key) {
            return sortOrder.value === 'asc' ? '↑' : '↓'
        }
        return ' '
    }
    const sortedData = computed(() => {
        return [...rawData.value].sort((a, b) => {
            const modifier = sortOrder.value === 'asc' ? 1 : -1
            return a[sortKey.value] > b[sortKey.value] ? modifier : -modifier
        })
    })
    const toggleSort = (key) => {
        if (sortKey.value === key) {
            sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
        } else {
            sortKey.value = key
            sortOrder.value = 'asc'
        }
    }

    // 同步滚动位置
    const headerScroll = ref(null)
    const bodyScroll = ref(null)
    const handleScroll = (e) => {
        headerScroll.value.scrollLeft = e.target.scrollLeft
    }

    // 定义列宽 计算标题基准宽度的方法
    const columnWidths = ref([220, 150])
    const dynamicWidths = ref([]);
    const calculateTitleWidth = () => {
        const containerWidth = tableContainer.value?.offsetWidth || 0
        if (!containerWidth) return

        const baseWidths = tableHeaders.value.map(header => Math.max(header.title.length * 13, 100))
        if(showScoreColumn.value) {
            baseWidths.push(120) // Score列固定宽度
        }
        // 需要补齐的情况
        const fixedWidth = columnWidths.value.reduce((sum, w) => sum + w, 0)
        const totalWidth = fixedWidth + baseWidths.reduce((sum, w) => sum + w, 0)
        if (totalWidth < containerWidth && baseWidths.length > 0) {
            const lastIndex = baseWidths.length - 1
            const remainWidth = containerWidth - (totalWidth - baseWidths[lastIndex])
            baseWidths[lastIndex] = Math.max(remainWidth, baseWidths[lastIndex])
        }

        dynamicWidths.value = baseWidths
    }
    const tableContainer = ref(null)

    const showRatioModal = ref(false)
    const ratioForm = ref({
        ia: 0.4,
        bio: 0.3,
        batch: 0.3
    })
    const overallScores = ref({})
    const showScoreColumn = ref(false)

    const calculateOverall = () => {
        const sum = Object.values(ratioForm.value).reduce((a, b) => a + b, 0)
    
        if (Math.abs(sum - 1) > 0.001) {
            alert('The sum of the proportions must equal 1.')
            return
        }

        // 计算加权平均
        overallScores.value = {}
        rawData.value.forEach(item => {
            const score = 
                (item.ia_overall * ratioForm.value.ia) +
                (item.bio_overall * ratioForm.value.bio) +
                (item.batch_overall * ratioForm.value.batch)
            
            item.score = score.toFixed(4)
        })
        showRatioModal.value = false
        showScoreColumn.value = true
        calculateTitleWidth()
        // 在 DOM 更新之后将滚动轴置于最右端
        nextTick(() => {
            const bodyScrollElement = bodyScroll.value;
            if (bodyScrollElement) {
                bodyScrollElement.scrollLeft = bodyScrollElement.scrollWidth;
            }
        });
    }

    


    // 生命周期
    onMounted(async () => {
        try {
            await new Promise(resolve => setTimeout(resolve, 500))
            rawData.value = await api.getEcoData(selectedType.value)
            headerScroll.value = document.querySelector('.ecoListTableHeadDiv')
            bodyScroll.value = document.querySelector('.ecoListTableBodyDiv')
            duniqueTypes.value = [...new Set(rawData.value.map(item => item.datasets))]
            duniqueTypes.value.sort()
            calculateTitleWidth()
        } catch (error) {
            console.error('Initial data load failed:', error)
        }
    })
</script>
  
<style scoped>
    .ecoList {
        padding-left: 20px;
        padding-right: 20px;
        padding-top: 5px;
        width: 100%;
        height:870px;
        margin: 0 auto;
        display: flex;
        flex-direction: column; /* 启用弹性布局 */
        
    }
    .ecoListTables{
        color: black;
        width: 100%;
        height: 100%;
        flex: 1; /* 占据剩余空间 */
        display: flex;
        flex-direction: column;
        overflow: hidden; /* 隐藏内部溢出 */
    }
    .ecoListTableHead, 
    .ecoListTableBody {
        table-layout: fixed;
        width: 100%;
        border-collapse: collapse;
        background-color: #fafafa;
        
    }
    .ecoListTableHeadDiv{
        flex-shrink: 0; /* 固定高度 */
        overflow: hidden;
        position: sticky; /* 固定表头 */
        top: 0;
        z-index: 1;
    }
    .ecoListTableBodyDiv{
        flex: 1;
        width: calc(100% + 17px);
        padding-right: 17px;
        overflow-x: scroll;
        overflow-y: auto; /* 保持滚动功能但隐藏滚动条 */
    }



    /* 移除绝对定位 */
    .ecoListTableHeadDiv,
    .ecoListTableBodyDiv {
        position: static;
    }

    /* 列宽同步处理 */
    .ecoListTableHead th,
    .ecoListTableBody td {
        box-sizing: border-box;
        padding: 12px 15px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        border: 0.1px solid #f1f1f1;
        text-align: center;
    }
    .ecoListTableHead th {
        cursor: pointer;
        user-select: none;
    }
    .ecoListTableHead th.active {
        background-color: #e1e1e1;
    }
    .ecoListTableBody tr:hover{
        background-color: #e1e1e1;
    }

    .sort-icon {
        margin-left: 3px;
    }

    /* 新增固定列样式 */
    .ecoListTableHead th:first-child,
    .ecoListTableBody td:first-child {
        position: sticky;
        left: 0;
        z-index: 2;
        background: #fafafa;
        box-shadow: 2px 0 4px rgba(0,0,0,0.1);
    }

    /* 表头固定列提升层级 */
    .ecoListTableHead th:first-child {
        z-index: 3;
        /* background: #2f3a4a; */
    }

    /* 下拉框样式 */
    .type-filter {
        background: #fafafa;
        border: 1px solid #4f536f;
        color: black;
        padding: 5px 5px;
        border-radius: 4px;
        font-size: 0.9em;
        width: 95%;
        margin: 2px 0;
    }

    .type-filter:focus {
        outline: none;
        border-color: #1A3F90;
        box-shadow: 0 0 3px rgba(24, 144, 255, 0.5);
    }
    .detail-link {
        color: #1A3F90;
        text-decoration: none;
        transition: color 0.3s;
    }

    .detail-link:hover {
        text-decoration: underline;
    }

    /* 模态框基础样式 */
    .modalRatio{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 2;
    }
    .modal-content {
        background: #2f3a4a;
        padding: 20px;
        border-radius: 8px;
        width: 400px;
        color: white;
    }

    .modal-title {
        margin: 0 0 20px;
        font-size: 16px;
    }

    /* 自定义表单样式 */
    .custom-form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .form-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .form-item label {
        width: 140px;
        font-size: 14px;
    }

    .form-item input {
        width: 180px;
        padding: 8px 12px;
        background: #3a4555;
        border: 1px solid #4f536f;
        border-radius: 4px;
        color: white;
        font-size: 14px;
    }

    input[type="number"]::-webkit-inner-spin-button {
        -webkit-appearance: none;
    }

    /* 错误提示 */
    .error-msg {
        color: #ff4d4f;
        font-size: 12px;
        text-align: center;
        height: 20px;
    }

    /* 按钮样式 */
    .form-actions {
        display: flex;
        justify-content: flex-end;
        gap: 10px;
        margin-top: 15px;
    }

    button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }

    .cancel-btn {
        background: #4f536f;
        color: white;
    }

    .submit-btn {
        background: #4d7398;
        color: white;
    }

    .submit-btn:disabled {
        background: #4f536f;
        cursor: not-allowed;
        opacity: 0.7;
    }
</style>