import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import store from './store';
import router from './router';
import * as VeeValidate from 'vee-validate';
import DisableAutocomplete from 'vue-disable-autocomplete';
import './components/styled-components';
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import 'bootstrap-vue/dist/bootstrap-vue-icons.min.css'
import 'bulma/css/bulma.css';
import './static/app.css';

let package = require('../package.json');

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VeeValidate, {
  // This is the default
  inject: true,
  // Important to name this something other than 'fields'
  fieldsBagName: 'veeFields',
  // This is not required but avoids possible naming conflicts
  errorBagName: 'veeErrors'
})
Vue.use(DisableAutocomplete);

Vue.config.productionTip = false
Vue.prototype.axios = axios
Vue.prototype.$apiUrl = package.envConfig.apiUrl;

new Vue({
  store,
  beforeCreate() {
    this.$store.commit('initializeStore');
	},
  router,
  render: h => h(App)
}).$mount('#app')
