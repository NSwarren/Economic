import { createRouter, createWebHistory } from 'vue-router'
import EcoList from '../components/EcoList.vue'
import DetailPage from '../components/DetailPage.vue'
import UploadFile from '../components/UploadFile.vue'
import Economy from '../components/Economy.vue'

const routes = [
    {
        path: '/',
        name: 'Economy',
        component: Economy
    },
    {
        path: '/detail/:name',
        name: 'Detail',
        component: DetailPage,
        props: true
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router