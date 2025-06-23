import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'
import Register from './components/register.vue'
import Login from './components/login.vue'
import Logout from './components/logout.vue'
import adminDashboard from './components/adminDashboard.vue'  
import EditLot from './components/editLot.vue'
import AddLot from './components/addLot.vue' 

axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'
axios.defaults.baseURL = 'http://localhost:5000'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  }
  ,
  {
    path: '/login',
    name: 'Login',
    component: Login
    
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout
  },
  {
    path: '/admin_dashboard',
    name: 'adminDashboard',
    component: adminDashboard
  },
  {
    path: '/admin_editlot/:lot_id',
    name: 'EditLot',  
    component: EditLot,
    props: true
  },
  {
    path: '/admin_addlot',
    name: 'AddLot',
    component: AddLot
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
