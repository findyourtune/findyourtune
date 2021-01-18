import Vue from 'vue';
import VueRouter from 'vue-router'

import Main from '../views/Main.vue'
import Courses from '../views/Courses.vue'

Vue.use(VueRouter)

export default new VueRouter({
    routes: [
      { path: '/', component: Main, props: { msg: 'Test Prop' } },
      { path: '/courses', component: Courses },
    ]
})