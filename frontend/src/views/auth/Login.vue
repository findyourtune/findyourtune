<template>
  <div>
    <b-form @submit.stop.prevent="onSubmit" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email"
        label-for="input-1"
      >
        <b-form-input
        id="input-1"
        name="input-1"
        v-model="form.email"
        type="email"
        placeholder="Enter email"
        v-validate="{ required: true, min: 5 }"
        :state="validateState('input-1')"
        aria-describedby="input-1-live-feedback"
        data-vv-as="Email"
        ></b-form-input>
        <b-form-invalid-feedback id="input-1-live-feedback">{{ veeErrors.first('input-1') }}</b-form-invalid-feedback>
      </b-form-group>

      <b-form-group id="input-group-2" label="Password" label-for="input-2">
        <b-input-group>
          <b-form-input
          ref="password"
          id="input-2"
          name="input-2"
          v-model="form.password"
          placeholder="Enter Password"
          v-validate="{ required: true, min: 8 }"
          :state="validateState('input-2')"
          aria-describedby="input-2-live-feedback"
          data-vv-as="Password"
          :type="passwordFieldType"
          ></b-form-input>
          <b-input-group-append is-text>
            <b-icon v-if="passwordFieldType === 'password'" class="default-button" @click="switchVisibility()" icon="eye-slash"></b-icon>
            <b-icon v-if="passwordFieldType === 'text'" class="default-button" @click="switchVisibility()" icon="eye"></b-icon>
          </b-input-group-append>
          <b-form-invalid-feedback id="input-2-live-feedback">{{ veeErrors.first('input-2') }}</b-form-invalid-feedback>
        </b-input-group>
      </b-form-group>

      <b-row class="function-row">
        <themed-btn class="login-btn" type="submit" variant="primary">Login</themed-btn>
        <router-link to="resetPassword">Forgot Password?</router-link>
      </b-row>
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
      this.$router.push('/u/' + this.$store.state.auth.user.username);
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
            this.$router.push('/u/' + this.$store.state.auth.user.username);
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
    },
    validateState(ref) {
      if (
        this.veeFields[ref] &&
        (this.veeFields[ref].dirty || this.veeFields[ref].validated)
      ) {
        return !this.veeErrors.has(ref);
      }
      return null;
    },
  }
};
</script>

<style scoped>
.function-row {
  align-items: center;
  margin-left: 0px !important;
}

.login-btn {
  margin-right: 15px;
}
</style>
