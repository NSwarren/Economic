import { createRouter, createWebHistory } from 'vue-router'
import EcoList from '../components/EcoList.vue'
import Details from '../components/Details.vue'
import UploadFile from '../components/UploadFile.vue'
import Economy from '../components/Economy.vue'
import EcoTable from '../components/EcoTable.vue'

const routes = [
    {
        path: '/',
        name: 'Economy',
        component: Economy,
        children:[{
            path: '',
            name: 'EcoTable',
            component: EcoTable,
            props: true
        },{
            path: '/detail/:name',
            name: 'ImageShow',
            component: Details,
            props: true
        }
        ]
    } 
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router