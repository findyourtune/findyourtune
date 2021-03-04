<template>
  <div>
    <b-form @submit.stop.prevent="onSubmit" v-if="show">
    <b-form-group
      id="input-group-1"
      label="First Name"
      label-for="input-1"
    >
      <b-form-input
        id="input-1"
        name="input-1"
        v-model="form.firstname"
        type="text"
        placeholder="Enter first name"
        v-validate="{ required: true, min: 2 }"
        :state="validateState('input-1')"
        aria-describedby="input-1-live-feedback"
        data-vv-as="First Name"
      ></b-form-input>
      <b-form-invalid-feedback id="input-1-live-feedback">{{ veeErrors.first('input-1') }}</b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
      id="input-group-2"
      label="Last Name"
      label-for="input-2"
    >
      <b-form-input
        id="input-2"
        name="input-2"
        v-model="form.lastname"
        type="text"
        placeholder="Enter last name"
        v-validate="{ required: true, min: 2 }"
        :state="validateState('input-2')"
        aria-describedby="input-2-live-feedback"
        data-vv-as="Last Name"
      ></b-form-input>
      <b-form-invalid-feedback id="input-2-live-feedback">{{ veeErrors.first('input-2') }}</b-form-invalid-feedback>
    </b-form-group>

     <b-form-group
      id="input-group-3"
      label="Username"
      label-for="input-3"
    >
      <b-form-input
        id="input-3"
        name="input-3"
        v-model="form.username"
        type="text"
        placeholder="Enter username"
        v-validate="{ required: true, min: 8 }"
        :state="validateState('input-3')"
        aria-describedby="input-3-live-feedback"
        data-vv-as="Username"
      ></b-form-input>
      <b-form-invalid-feedback id="input-3-live-feedback">{{ veeErrors.first('input-3') }}</b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
      id="input-group-4"
      label="Email"
      label-for="input-4"
    >
      <b-form-input
        id="input-4"
        name="input-4"
        v-model="form.email"
        type="email"
        placeholder="Enter email"
        v-validate="{ required: true, min: 5 }"
        :state="validateState('input-4')"
        aria-describedby="input-4-live-feedback"
        data-vv-as="Email"
      ></b-form-input>
      <b-form-invalid-feedback id="input-4-live-feedback">{{ veeErrors.first('input-4') }}</b-form-invalid-feedback>
    </b-form-group>

    <b-form-group id="input-group-5" label="Password" label-for="input-5">
      <b-input-group>
        <b-form-input
        ref="password"
        id="input-5"
        name="input-5"
        v-model="form.password"
        placeholder="Enter Password"
        v-validate="{ required: true, min: 8 }"
        :state="validateState('input-5')"
        aria-describedby="input-5-live-feedback"
        data-vv-as="Password"
        :type="passwordFieldType"
        ></b-form-input>
        <b-input-group-append is-text>
          <b-icon v-if="passwordFieldType === 'password'" class="default-button" @click="switchVisibility()" icon="eye-slash"></b-icon>
          <b-icon v-if="passwordFieldType === 'text'" class="default-button" @click="switchVisibility()" icon="eye"></b-icon>
        </b-input-group-append>
        <b-form-invalid-feedback id="input-5-live-feedback">{{ veeErrors.first('input-5') }}</b-form-invalid-feedback>
      </b-input-group>
    </b-form-group>

    <b-form-group id="input-group-6" label="Confirm Password" label-for="input-6">
      <b-input-group>
        <b-form-input
        id="input-6"
        name="input-6"
        v-model="form.confirmPassword"
        placeholder="Re-enter Password"
        v-validate="{ required: true, min: 8, confirmed: 'password' }"
        :state="validateState('input-6')"
        aria-describedby="input-6-live-feedback"
        data-vv-as="Confirm Password"
        :type="passwordFieldType"
        ></b-form-input>
        <b-input-group-append is-text>
          <b-icon v-if="passwordFieldType === 'password'" class="default-button" @click="switchVisibility()" icon="eye-slash"></b-icon>
          <b-icon v-if="passwordFieldType === 'text'" class="default-button" @click="switchVisibility()" icon="eye"></b-icon>
        </b-input-group-append>
        <b-form-invalid-feedback id="input-6-live-feedback">{{ veeErrors.first('input-6') }}</b-form-invalid-feedback>
      </b-input-group>
    </b-form-group>

    <themed-btn type="submit" variant="primary">Sign Up</themed-btn>
    <!-- <button class="btn btn-primary" type="submit">Sign Up</button> -->
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
  name: 'Register',
  data() {
    return {
      form: {
        firstname: '',
        lastname: '',
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
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
      this.$router.push('/u/' + this.$store.state.auth.user.username);
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
          this.$store.dispatch('auth/register', this.form).then(
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