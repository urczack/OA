import {createRouter, createWebHashHistory} from 'vue-router'


const routes = [
    {
        path: '/login',
        name: 'login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/',
        name: '',
        component: () => import('../layout/index.vue')
    }
]


const router = createRouter({
    history: createWebHashHistory(),
    routes
})


export default router




