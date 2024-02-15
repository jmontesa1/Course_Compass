import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './main.css' //Global CSS for Font
import NavBar from './components/NavBar.vue'

createApp(App).use(router).mount('#app')
