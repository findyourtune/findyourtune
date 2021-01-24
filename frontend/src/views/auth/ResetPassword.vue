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

      <themed-btn type="submit" variant="primary">Request Password Reset</themed-btn>
    </b-form>

    <div
      v-if="message"
      class="alert"
      :class="successful ? 'alert-success' : 'alert-danger'"
    >{{message}}</div>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  data() {
    return {
      loading: false,
      message: '',
      successful: '',
      form: {
          email: ''
      },
      show: true,
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
    onSubmit() {
      this.loading = true;
      this.$validator.validateAll().then(isValid => {
        if (!isValid) {
        this.loading = false;
        return;
        }

        if (this.form.email) {
        this.$store.dispatch('auth/passwordReset', this.form).then(
          () => {
          this.$router.push('/login');
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
