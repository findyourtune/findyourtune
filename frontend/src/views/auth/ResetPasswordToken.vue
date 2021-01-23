<template>
  <div>
    <b-form @submit="onSubmit" v-if="show">

    <b-form-group id="input-group-3" label="Password:" label-for="input-3">
      <b-input-group>
        <b-form-input
        id="input-3"
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

    <b-form-group id="input-group-4" label="Confirm Password:" label-for="input-4">
      <b-input-group>
        <b-form-input
        id="input-4"
        v-model="form.confirmPassword"
        placeholder="Re-enter Password"
        v-validate="'required'"
        :type="passwordFieldType"
        ></b-form-input>
        <b-input-group-append is-text>
          <b-icon v-if="passwordFieldType === 'password'" class="view-password-btn" @click="switchVisibility()" icon="eye-slash"></b-icon>
          <b-icon v-if="passwordFieldType === 'text'" class="view-password-btn" @click="switchVisibility()" icon="eye"></b-icon>
        </b-input-group-append>
      </b-input-group>
    </b-form-group>

    <themed-btn type="submit" variant="primary">Update Password</themed-btn>
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
  name: 'ResetPasswordToken',
  data() {
    return {
      form: {
        password: '',
        confirmPassword: '',
        token: ''
      },
      show: true,
      passwordFieldType: 'password',
      submitted: false,
      successful: false,
      message: ''
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
      this.message = '';
      this.submitted = true;
      this.$validator.validate().then(isValid => {
        if (isValid) {
          this.form.token = this.$route.params.token;
          this.$store.dispatch('auth/passwordResetToken', this.form).then(
            () => {
                this.$router.push('/login');
            },
            error => {
              this.message =
                (error.response && error.response.data) ||
                error.message ||
                error.toString();
              this.successful = false;
            }
          );
        }
      });
    }
  }
};
</script>