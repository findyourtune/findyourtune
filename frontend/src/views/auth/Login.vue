<template>
  <div>
    <b-form @submit="onSubmit" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email:"
        label-for="input-1"
      >
        <b-form-input
        id="input-1"
        v-model="form.email"
        type="email"
        placeholder="Enter email"
        v-validate="'required'"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Password:" label-for="input-2">
        <b-input-group>
          <b-form-input
          id="input-2"
          v-model="form.password"
          placeholder="Enter Password"
          v-validate="'required'"
          :type="passwordFieldType"
          ></b-form-input>
          <b-input-group-append is-text>
            <b-icon v-if="passwordFieldType === 'password'" class="view-password-btn" @click="switchVisibility()" icon="eye-slash"></b-icon>
            <b-icon v-if="passwordFieldType === 'text'" class="view-password-btn" @click="switchVisibility()" icon="eye"></b-icon>
          </b-input-group-append>
        </b-input-group>
      </b-form-group>

      <themed-btn type="submit" variant="primary">Login</themed-btn>
      <router-link to="resetPassword">Forgot Password?</router-link>
    </b-form>
    <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card>

    <div
      v-if="message"
      class="alert"
      :class="successful ? 'alert-success' : 'alert-danger'"
    >{{message}}</div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loading: false,
      message: '',
      successful: '',
      form: {
          email: '',
          password: ''
      },
      show: true,
      passwordFieldType: 'password'
    };
  },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    }
  },
  mounted() {
    if (this.loggedIn) {
      this.$router.push('/profile');
    }
  },
  methods: {
    switchVisibility() {
      this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
    },
    onSubmit() {
      this.loading = true;
      this.$validator.validateAll().then(isValid => {
        if (!isValid) {
        this.loading = false;
        return;
        }

        if (this.form.email && this.form.password) {
        this.$store.dispatch('auth/login', this.form).then(
          () => {
            this.$router.push('/profile');
          },
          error => {
          this.loading = false;
          this.successful = false;
          this.message =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
        );
        }
      });
    }
  }
};
</script>
