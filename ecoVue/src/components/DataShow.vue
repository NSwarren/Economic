<template>
  <div class="detailContainer">
    <div class="header-container">
      <h2>{{ item.name }} 详情</h2>
      <router-link to="/" class="back-button">
        <span>&lt;</span>
      </router-link>
    </div>
    <div class="table-wrapper">
      <table class="metric-table">
        <thead>
          <tr>
            <th class="metric-header">指标</th>
            <th v-for="dataset in datasets" :key="dataset" class="dataset-header">
              {{ dataset }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="metric in metrics" :key="metric.key">
            <td class="metric-label">{{ metric.label }}</td>
            <td v-for="dataset in datasets" :key="dataset" class="metric-value">
              {{ getMetricValue(metric.key, dataset) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import api from '@/services/api'

  const route = useRoute()
  const item = ref({})
  const rawData = ref([])

  // 指标显示配置
  const metricConfig = [
    { key: 'mean_average_precision', label: 'Mean Average Precision' },
    { key: 'normalized_mutual_info', label: 'Normalized Mutual Info' },
    { key: 'avg_silhouette_width', label: 'Avg Silhouette Width' },
    { key: 'ari', label: 'Adjusted Rand Index' }
  ]

  // 计算属性
  const datasets = computed(() => {
    return [...new Set(rawData.value.map(item => item.datasets))].sort()
  })

  const metrics = computed(() => {
    return metricConfig.map(config => ({
      ...config,
      values: datasets.value.map(dataset => {
        const data = rawData.value.find(d => d.datasets === dataset)
        return data ? data[config.key] : '-'
      })
    }))
  })

  // 获取指标值
  const getMetricValue = (key, dataset) => {
    const data = rawData.value.find(d => d.datasets === dataset)
    return data ? data[key]?.toFixed(4) || '-' : '-'
  }

  // 获取数据
  onMounted(async () => {
    try {
      const response = await api.getDetail(route.params.name)
      rawData.value = response // 假设返回的是该方法的全部数据集数据
      item.value = response[0] || {}
    } catch (error) {
      console.error('获取详情失败:', error)
    }
  })
</script>

<style scoped>
  .detailContainer {
    width: 85%;
    margin: 20px auto;
    padding: 20px;
    background: #28313E;
    color: white;
    border-radius: 8px;
  }

  .table-wrapper {
    overflow-x: auto;
  }

  th, td {
    padding: 12px 15px;
    border: 1px solid #4f536f;
    text-align: center;
  }

  /* 固定第一列宽度 */
  .metric-table th:first-child,
  .metric-table td:first-child {
    width: 200px; /* 固定宽度值 */
    min-width: 200px; /* 防止压缩 */
    max-width: 200px; /* 防止扩展 */
    text-align: left;
    padding-left: 20px;
    position: sticky;
    left: 0;
    z-index: 1;
  }

  /* 其他列自适应 */
  .metric-table th:not(:first-child),
  .metric-table td:not(:first-child) {
    width: auto;
    min-width: 120px; /* 保留最小宽度 */
  }

  .metric-header {
    background: #434654;
    font-weight: bold;
  }

  .dataset-header {
    background: #3a4455;
    color: #05E89D;
  }

  .metric-label {
    text-align: left;
    background: #434654;
    font-weight: bold;
  }

  .metric-value {
    background: #2f3a4a;
  }

  tr:hover td {
    background-color: #454856;
  }

  .header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
    padding: 0 15px;
  }

  .back-button {
    background: #434654;
    color: #05E89D;
    padding: 8px 15px;
    border-radius: 4px;
    text-decoration: none;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 5px;
    border: 1px solid #05E89D55;
  }

  .back-button span {
    font-weight: bold;
    font-size: 1.1em;
  }

  .back-button:hover {
    background: #05E89D22;
    box-shadow: 0 0 8px #05E89D33;
    transform: translateY(-1px);
  }


</style>