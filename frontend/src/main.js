import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import BootstrapVue from "bootstrap-vue";
import store from './store';
import router from './router';
import './components/styled-components';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bulma/css/bulma.css';

Vue.use(BootstrapVue);

Vue.config.productionTip = false
Vue.prototype.axios = axios


new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
