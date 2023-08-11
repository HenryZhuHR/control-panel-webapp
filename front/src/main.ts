import { createApp } from 'vue'
import './style.css'
import App from './App.vue'


// 引入组件库的少量全局样式变量
import 'tdesign-mobile-vue/es/style/index.css';

const app = createApp(App);
app.mount('#app');


