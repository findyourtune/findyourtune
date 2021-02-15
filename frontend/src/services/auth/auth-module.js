// Authorization Module containing auth states/methods
import AuthService from '../auth/auth-service';

const user = JSON.parse(localStorage.getItem('user'));
const initialState = user
  ? { status: { loggedIn: true }, user }
  : { status: { loggedIn: false }, user: null };

export const auth = {
  namespaced: true,
  state: initialState,
  actions: {
    login({ commit }, user) {
      return AuthService.login(user).then(
        user => {
          commit('loginSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('loginFailure');
          return Promise.reject(error);
        }
      );
    },
    logout({ commit }) {
      AuthService.logout();
      commit('logout');
    },
    register({ commit }, user) {
      return AuthService.register(user).then(
        response => {
          commit('registerSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('registerFailure');
          return Promise.reject(error);
        }
      );
    },
    passwordReset({ commit }, user) {
      return AuthService.passwordReset(user).then(
        response => {
          commit('passwordResetSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('passwordResetFailure');
          return Promise.reject(error);
        }
      );
    },
    passwordResetToken({ commit }, user) {
      return AuthService.passwordResetToken(user).then(
        response => {
          commit('passwordResetTokenSuccess');
          return Promise.resolve(response.data);
        },
        error => {
          commit('passwordResetTokenFailure');
          return Promise.reject(error);
        }
      );
    },
    updateProfile({ commit }, user) {
      return AuthService.updateProfile(user).then(
        user => {
          commit('updateProfileSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('updateProfileFailure');
          return Promise.reject(error);
        }
      );
    },
    updateAppColor({ commit }, user) {
      return AuthService.updateAppColor(user).then(
        user => {
          commit('updateAppColorSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('updateAppColorFailure');
          return Promise.reject(error);
        }
      );
    },
    updateSpotifyAccount({ commit }, user) {
      return AuthService.updateSpotifyAccount(user).then(
        user => {
          commit('updateSpotifyAccountSuccess', user);
          return Promise.resolve(user);
        },
        error => {
          commit('updateSpotifyAccountFailure');
          return Promise.reject(error);
        }
      );
    },
  },
  mutations: {
    loginSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    loginFailure(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    logout(state) {
      state.status.loggedIn = false;
      state.user = null;
    },
    registerSuccess(state) {
      state.status.loggedIn = false;
    },
    registerFailure(state) {
      state.status.loggedIn = false;
    },
    passwordResetSuccess(state) {
      state.status.loggedIn = false;
    },
    passwordResetFailure(state) {
      state.status.loggedIn = false;
    },
    passwordResetTokenSuccess(state) {
      state.status.loggedIn = false;
    },
    passwordResetTokenFailure(state) {
      state.status.loggedIn = false;
    },
    updateProfileSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    updateProfileFailure(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    updateAppColorSuccess(state) {
      state.status.loggedIn = true;
    },
    updateAppColorFailure(state) {
      state.status.loggedIn = true;
    },
    updateSpotifyAccountSuccess(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    },
    updateSpotifyAccountFailure(state, user) {
      state.status.loggedIn = true;
      state.user = user;
    }
  }
};