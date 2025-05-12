import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

const uploadAPI = 'http://127.0.0.1:8000/upload'; 

export default {
  async getEcoData(datatype) {
    try {
      const response = await api.get(`/dataList/${datatype}`)
      console.log(response)
      return response.data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  async getDetail(name) {
    try {
      const response = await api.get(`/details/${name}`)
      console.log(response)
      return response.data
    } catch (error) {
      console.error('API Error:', error)
      throw error
    }
  },

  async uploadFiles(files){
    try {
      const response = await api.post('upload', files, {
        headers: {
          'Content-Type': 'multipart/form-data' // 必须设置
        }
      });

      console.log(response)

      if (response.data.success) {
        return true;
      }
    } catch (error) {
      return false;
    }
  }
}