// Services for auth module to access
import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://127.0.0.1/api/auth/';

class AuthService {
  login(form) {
    return axios
      .post(API_URL + 'login', {
        email: form.email,
        password: form.password
      })
      .then(response => {
        if (response.data.access_token) {
          localStorage.user = JSON.stringify(response.data);
        }

        return response.data;
      });
  }

  logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('appColor');
  }

  register(form) {
    return axios.post(API_URL + 'register', {
      firstname: form.firstname,
      lastname: form.lastname,
      username: form.username,
      email: form.email,
      password: form.password,
      confirmPassword: form.confirmPassword
    });
  }

  passwordReset(form) {
    return axios.post(API_URL + 'reset_password', {
      email: form.email,
    });
  }

  passwordResetToken(form) {
    return axios.post(API_URL + 'reset_password_token', {
      token: form.token,
      password: form.password,
      confirmPassword: form.confirmPassword
    });
  }

  updateProfile(form) {
    return axios.post(API_URL + 'update_profile', {
      firstname: form.firstname,
      lastname: form.lastname,
      username: form.username,
      email: form.email
    }, { headers: authHeader() })
    .then(response => {
      if (response.data.access_token) {
        localStorage.user = JSON.stringify(response.data);
      }

      return response.data;
    });
  }
}

export default new AuthService();
