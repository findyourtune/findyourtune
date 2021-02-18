// Services for auth module to access
import axios from 'axios';
import authHeader from './auth-header';
import store from '../../store';
let package = require('../../../package.json');
const AUTH_URL = package.envConfig.apiUrl + '/api/auth/';

class AuthService {
  login(form) {
    return axios
      .post(AUTH_URL + 'login', {
        email: form.email,
        password: form.password
      })
      .then(response => {
        if (response.data.access_token) {
          localStorage.user = JSON.stringify(response.data);
        }

        if (response.data.appcolor) {
          store.commit('setAppColor', response.data.appcolor) 
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('appColor');
  }

  register(form) {
    return axios.post(AUTH_URL + 'register', {
      firstname: form.firstname,
      lastname: form.lastname,
      username: form.username,
      email: form.email,
      password: form.password,
      confirmPassword: form.confirmPassword
    });
  }

  passwordReset(form) {
    return axios.post(AUTH_URL + 'reset_password', {
      email: form.email,
    });
  }

  passwordResetToken(form) {
    return axios.post(AUTH_URL + 'reset_password_token', {
      token: form.token,
      password: form.password,
      confirmPassword: form.confirmPassword
    });
  }

  updateProfile(form) {
    return axios.post(AUTH_URL + 'update_profile', {
      firstname: form.firstname,
      lastname: form.lastname,
      username: form.username,
      email: form.email,
      bio: form.bio
    }, { headers: authHeader() })
    .then(response => {
      if (response.data.access_token) {
        localStorage.user = JSON.stringify(response.data);
      }

      return response.data;
    });
  }

  updateAppColor(form) {
    return axios.post(AUTH_URL + 'update_appcolor', {
      appcolor: form.appcolor,
      username: form.username
    }, { headers: authHeader() })
    .then(response => {
      return response.data;
    });
  }

  updateSpotifyAccount(form) {
    return axios.post(AUTH_URL + 'link_spotify', {
      spotify_account: form.spotify_account,
      username: form.username
    }, { headers: authHeader() } )
    .then(response => {
      if(response.data.auth_url) {
        window.location.href = response.data.auth_url;
      }
      return response.data;
    });
  }
}

export default new AuthService();
