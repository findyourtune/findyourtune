import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import store from './store';
import router from './router';
import * as VeeValidate from 'vee-validate';
import './components/styled-components';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.min.css'
import 'bulma/css/bulma.css';
import './static/app.css';

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VeeValidate);

Vue.config.productionTip = false
Vue.prototype.axios = axios


new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
