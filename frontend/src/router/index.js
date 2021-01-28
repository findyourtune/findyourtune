import Vue from 'vue';
import VueRouter from 'vue-router'

import Main from '../views/Main.vue'
import Courses from '../views/Courses.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Profile from '../views/auth/Profile.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/', component: Main, props: { msg: 'Test Prop' }, name: 'home' },
    { path: '/courses', component: Courses, name: 'courses' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/profile', component: Profile, name: 'profile' },
    {
      path: '/resetPassword',
      name: 'resetPassword',
      component: () => import('../views/auth/ResetPassword.vue')
    },
    {
      path: '/resetPasswordToken/:token',
      name: 'resetPasswordToken',
      component: () => import('../views/auth/ResetPasswordToken.vue')
    }
  ]
}) 

// publicPages are paths in the router that should not require user authentication
router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/', '/resetPassword', '/resetPasswordToken/:token'];
  const authRequired = !publicPages.includes(to.path);
  const loggedIn = localStorage.getItem('user');

  // if a user tries to access any other path then they'll be redirected to login
  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;