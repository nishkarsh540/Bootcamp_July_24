import { createRouter, createWebHistory } from 'vue-router'
import store from '../store';
import HomeView from '../views/HomeView.vue'
import UserSignup from '../views/UserSignup.vue'
import LoginUser from '../views/LoginUser.vue'
import UserDashboard from '../views/UserDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import CategoryManagment from '../views/CategoryManagment.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/category',
    name: 'category',
    component: CategoryManagment,
    meta:{requiresAuth:true,roles:['admin']}
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser,
    meta: {requiresGuest: true}
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignup,
    meta: {requiresGuest:true}
  },
  {
    path: '/admin-dashboard',
    name: 'admin',
    component: AdminDashboard,
    meta:{ requiresAuth:true,roles:['admin']}
  },
  {
    path: '/user-dashboard',
    name: 'user',
    component: UserDashboard,
    meta: {requiresAuth:true,roles:['user']}
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to,from ,next)=>{
    if (to.meta.requiresAuth){
      if (!store.getters.isAuthenticated){
        next('/login');
      } else {
        const userRole = store.getters.userRole;
        if(to.meta.roles && !to.meta.roles.includes(userRole)){
          next('/');
        } else {
          next();
        }
      }
    } else if (to.meta.requiresGuest && store.getters.isAuthenticated){
      next('/');
    } else {
      next();
    }
})

export default router
