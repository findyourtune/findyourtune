<template>
  <div class="container">
    <b-form @submit="onSubmit" v-if="show">
        <b-form-group
        id="input-group-1"
        label="First Name:"
        label-for="input-1"
        >
        <b-form-input
            id="input-1"
            v-model="form.firstname"
            type="text"
            v-validate="'required'"
        ></b-form-input>
        </b-form-group>

        <b-form-group
        id="input-group-2"
        label="Last Name:"
        label-for="input-2"
        >
        <b-form-input
            id="input-2"
            v-model="form.lastname"
            type="text"
            v-validate="'required'"
        ></b-form-input>
        </b-form-group>

        <b-form-group
        id="input-group-3"
        label="Username:"
        label-for="input-3"
        >
        <b-form-input
            id="input-3"
            v-model="form.username"
            type="text"
            v-validate="'required|min:3|max:20'"
        ></b-form-input>
        </b-form-group>

        <b-form-group
        id="input-group-4"
        label="Email:"
        label-for="input-4"
        >
        <b-form-input
            id="input-4"
            v-model="form.email"
            type="email"
            v-validate="'required'"
        ></b-form-input>
        </b-form-group>

    <avatar/>
    <br />

    <themed-btn type="submit" variant="primary">Save</themed-btn>
    </b-form>
  </div>
</template>

<script>
import Avatar from '@/components/Avatar';

export default {
  name: 'editProfile',
  components: {
       'Avatar': Avatar
   },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    }
  },
  data() {
    return {
      loading: false,
      message: '',
      successful: '',
      form: {
          firstname: '',
          lastname: '',
          email: '',
          username: ''
      },
      show: true,
    };
  },
  created() {
    this.form.firstname = this.$store.state.auth.user.firstname;
    this.form.lastname = this.$store.state.auth.user.lastname;
    this.form.email = this.$store.state.auth.user.email;
    this.form.username = this.$store.state.auth.user.username;
  },
  mounted() {
    if (!this.loggedIn) {
      this.$router.push('/login');
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

        if (this.form.email && this.form.username) {
         this.$store.dispatch('auth/updateProfile', this.form).then(
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
    },
  }
};
</script>