import Vue from 'vue';
import VueRouter from 'vue-router'

import Main from '../views/Main.vue'
import About from '../views/About.vue'
import Search from '../views/Search.vue'
import Login from '../views/auth/Login.vue'
import Register from '../views/auth/Register.vue'
import Profile from '../views/auth/Profile.vue'
import ResetPassword from '../views/auth/ResetPassword.vue'
import ResetPasswordToken from '../views/auth/ResetPasswordToken.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/', component: Main, props: { msg: 'Home' }, name: 'home' },
    { path: '/about', component: About, name: 'about' },
    { path: '/search', component: Search, name: 'search' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/register', component: Register, name: 'register' },
    { path: '/u/:username', component: Profile, name: 'profile' },
    { path: '/resetPassword', component: ResetPassword, name: 'resetPassword' },
    { path: '/resetPasswordToken/:token', component: ResetPasswordToken, name: 'resetPasswordToken' },
  ]
}) 

// publicPages are paths in the router that should not require user authentication
router.beforeEach((to, from, next) => {
  const publicPages = ['login', 'register', 'home', 'resetPassword', 'resetPasswordToken', 'about'];
  const authRequired = !publicPages.includes(to.name);
  const loggedIn = localStorage.getItem('user');

  // if a user tries to access any other path then they'll be redirected to login
  if (authRequired && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;