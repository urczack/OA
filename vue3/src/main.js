import { createApp } from 'vue'
import App from './App.vue'
import SvgIcon from '@/icons'
import ElementPlus from 'element-plus'
import router from './router'
import 'element-plus/dist/index.css'
import '@/assets/style/border.css'
import '@/assets/style/reset.css'
import '@/router/index'


//createApp(App).use(ElementPlus).use(router).mount('#app')

const app = createApp(App)

SvgIcon(app)
app.use(ElementPlus)
app.use(router)
app.mount('#app')
