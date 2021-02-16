import Vue from 'vue';
import Vuex from 'vuex';
import { auth } from '../services/auth/auth-module'

Vue.use(Vuex);

const defaultAppColor = '#34bbe6';
const lightColor = '#f8f8f8';
const darkColor = '#303030';
// TODO: choose default value
const state = {
  appColor: defaultAppColor,
  themeColor: darkColor,
  theme: 'dark',
  defaultAppColor: defaultAppColor
};

const mutations = {
  initializeStore(state) {
    if (localStorage.getItem('appColor')) {
      state.appColor = localStorage.getItem('appColor');
    }

    let htmlElement = document.documentElement;
    if (localStorage.getItem('theme')) {
      state.theme = localStorage.getItem('theme')
      if (state.theme == 'light') {
        state.themeColor = lightColor;
      }
    } else {
      localStorage.theme = state.theme;
    }
    htmlElement.setAttribute('data-theme', state.theme);
  },
  setAppColor(state, color) {
    state.appColor = color;
    localStorage.appColor = color;
  },
  toggleTheme() {
      if(state.theme) {
          let htmlElement = document.documentElement;
          if (state.theme == 'light') {
              htmlElement.setAttribute('data-theme', 'dark');
              localStorage.theme = 'dark';
              state.theme = 'dark';
              state.themeColor = darkColor;
          } else {
              htmlElement.setAttribute('data-theme', 'light');
              localStorage.theme = 'light';
              state.theme = 'light';
              state.themeColor = lightColor;
          }
      }
  },
  setDefaultAppColor() {
    state.appColor = defaultAppColor;
  },
};

const getters = {
  appColor: state => state.appColor,
  themeColor: state => state.themeColor,
};

export default new Vuex.Store({
  state,
  mutations,
  getters,
  modules: {
    auth
  }
});