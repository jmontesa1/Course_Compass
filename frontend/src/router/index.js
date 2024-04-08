import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import About from '../views/AboutView.vue'
import Courses from '../views/CoursesView.vue'
import Schedule from '../views/ScheduleView.vue'
import Progress from '../views/ProgressView.vue'
import Login from '../views/LoginView.vue'
import Signup from '../views/SignupView.vue'
import MyAccount from '../views/MyAccountView.vue'
import Dashboard from '../views/DashboardView.vue'
import ChangePassword from '../views/ChangePasswordView.vue'
import AdminDashboard from '../views/AdminDashboardView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/about',
    name: 'about',
    component: About
  },
  {
    path: '/courses',
    name: 'courses',
    component: Courses
  },
  {
    path: '/schedule',
    name: 'schedule',
    component: Schedule
  },
  {
    path: '/progress',
    name: 'progress',
    component: Progress
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/signup',
    name: 'signup',
    component: Signup
  },
  {
    path: '/myaccount',
    name: 'myaccount',
    component: MyAccount
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/changepassword',
    name: 'changepassword',
    component: ChangePassword
  },
  {
    path: '/admin-dashboard',
    name: 'admindashboard',
    component: AdminDashboard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
