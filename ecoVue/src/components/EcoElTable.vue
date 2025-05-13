<template>
<div class="ecoList">
    <el-table :data="filteredData" height="250" style="width: 100%">
        <el-table-column prop="methods" label="Method" width="150" />
        <el-table-column prop="datasets"  width="150" >
            <!-- <select v-model="dselectedType" class="type-filter">
                <option value="">Datasets</option>
                <option v-for="type in duniqueTypes" :key="type" :value="type">
                    {{ type }}
                </option>
            </select> -->
        </el-table-column>
        <el-table-column label="Integration Accuracy">
            <el-table-column  label = "Mean Average Precision" prop = "mean_average_precision" width = "120"  />
            <el-table-column  label = "Normalized Mutual Info" prop = "normalized_mutual_info" width = "120"  />
            <el-table-column  label = "Avg Silhouette Width" prop = "avg_silhouette_width" width = "120"  />
            <el-table-column  label = "ARI" prop = "ari" width = "120"  />
            <el-table-column  label = "overall" prop = "ia_overall" width = "120"  />
        </el-table-column>
        <el-table-column label="Bio Conservation">
            <el-table-column label = "Traj Conserv" prop = "traj_conserv" />
            <el-table-column label = "Biomarker" prop = "biomarker" />
            <el-table-column label = "DARs" prop = "dars" />
            <el-table-column label = "Enriched Motif" prop = "enriched_motif" />
            <el-table-column label = "Overall" prop = "bio_overall" />
        </el-table-column>
        <el-table-column label="Batch Correction">
            <el-table-column label = "Ilisi" prop = "ilisi" />
            <el-table-column label = "Kbet" prop = "kbet" />
            <el-table-column label = "Graph Connectivity" prop = "graph_connectivity" />
            <el-table-column label = "Avg Silhouette Width Batch" prop = "avg_silhouette_width_batch" />
            <el-table-column label = "Overall" prop = "batch_overall" />
        </el-table-column>
    </el-table>
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
            { title: 'DARs' , key: 'dars', sortable: true },
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
    // const uniqueTypes = ref(['Integration Accuracy', 'Trajectory', 'Biomarker'])
    // 新增watch监听selectedType变化
    // watch(selectedType, async (newType) => {
    //     try {
    //         rawData.value = await api.getEcoData(newType)
    //         tableHeaders.value = metricHeaders[selectedType.value].value
    //         calculateTitleWidth()
    //         // 重置状态
    //         sortKey.value = 'name'
    //         sortOrder.value = 'asc'
    //         dselectedType.value = ''

    //     } catch (error) {
    //         console.error('Failed to fetch data:', error)
    //     }
    // })
    // 动态表头计算
    // const tableHeaders = computed(() => [
    // ...(metricHeaders[selectedType.value] || []),
    // ...duniqueTypes.value = [...new Set(rawData.value.map(item => item.datasets))]
    // ])

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
    const columnWidths = ref([150, 150])
    const dynamicWidths = ref([]);
    const calculateTitleWidth = () => {
        const containerWidth = tableContainer.value?.offsetWidth || 0
        if (!containerWidth) return

        const baseWidths = tableHeaders.map(header => Math.max(header.title.length * 11, 100))

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

    // 生命周期
    onMounted(async () => {
        try {
            await new Promise(resolve => setTimeout(resolve, 500))
            rawData.value = await api.getEcoData(selectedType.value)
            headerScroll.value = document.querySelector('.ecoListTableHeadDiv')
            bodyScroll.value = document.querySelector('.ecoListTableBodyDiv')
            // uniqueTypes.value.sort()
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
        padding: 20px;
        width: 100%;
        margin: 0 auto;
        color: black;
        display: flex;
        flex-direction: column; /* 启用弹性布局 */
        height: 100px;
    }

    .ecoListTables{
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
        background-color: #28313E;
    }
    .ecoListTableHeadDiv{
        flex-shrink: 0; /* 固定高度 */
        overflow: hidden;
    }
    .ecoListTableBodyDiv{
        flex: 1;
        overflow-y: auto; /* 内容区域滚动 */
        width: 100%; /* 移除之前增加的宽度 */
        padding-right: 0; /* 移除多余的填充 */
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
        border: 0.1px solid #4f536f;
        text-align: left;
    }
    .ecoListTableHead th {
        cursor: pointer;
        user-select: none;
    }
    .ecoListTableHead th.active {
        background-color: #434654;
    }
    .ecoListTableBody tr:hover{
        background-color: #454856;
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
        background: #2f3a4a;
        box-shadow: 2px 0 4px rgba(0,0,0,0.1);
    }

    /* 表头固定列提升层级 */
    .ecoListTableHead th:first-child {
        z-index: 3;
        /* background: #2f3a4a; */
    }

    /* 下拉框样式 */
    .type-filter {
        background: #2f3a4a;
        border: 1px solid #4f536f;
        color: white;
        padding: 5px 5px;
        border-radius: 4px;
        font-size: 0.9em;
        width: 95%;
        margin: 2px 0;
    }

    .type-filter:focus {
        outline: none;
        border-color: #1890ff;
        box-shadow: 0 0 3px rgba(24, 144, 255, 0.5);
    }
    .detail-link {
        color: #05E89D;
        text-decoration: none;
        transition: color 0.3s;
    }

    .detail-link:hover {
        text-decoration: underline;
    }
</style>