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
import viewspot from './components/viewspot.vue'
import viewreserveSpot from './components/adminReservespot.vue'
import AdminUsers from './components/adminusers.vue'
import userDashboard from './components/userDashboard.vue'
import userProfile from './components/userProfile.vue'
import userHistory from './components/userHistory.vue'
import userRelease from './components/userRelease.vue'
import UserBook from './components/userbook.vue'
import AdminSummary from './components/adminSummary.vue'
import UserSummary from './components/userSummary.vue'
import AdminSearch from './components/adminSearch.vue'

axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept'] = 'application/json'
 axios.defaults.baseURL = 'http://localhost:5000'; 
axios.defaults.withCredentials = true; 

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
  },
  {
    path: '/admin_viewspot/:spot_id',
    name: 'viewspot',
    component: viewspot,
  },
  {
    path:'/admin_reservespot/:spot_id',
    name:'viewreserveSpot',
    component: viewreserveSpot
  },
  {
    path:'/admin_users',
    name:'AdminUsers',
    component: AdminUsers
  },
  {
    path: '/user_dashboard',
    name: 'userDashboard',
    component: userDashboard
  },
  {
    path: '/user_profile',
    name: 'userProfile',
    component: userProfile
  },
  {
    path: '/user_history',
    name: 'userHistory',
    component: userHistory
  },
  {
    path: '/user_release/:r_id',
    name: 'userRelease',
    component: userRelease
  },
  {
    path: '/user_book/:lot_id',
    name: 'UserBook',
    component: UserBook
  },
  {
    path: '/admin_summary',
    name: 'AdminSummary',
    component: AdminSummary
  },
  {
    path: '/user_summary',
    name: 'UserSummary',
    component: UserSummary
  },
  {
    path: '/admin_search',
    name: 'AdminSearch',
    component: AdminSearch
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
