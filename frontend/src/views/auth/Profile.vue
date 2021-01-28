<template>
  <div class="container">
    <b-jumbotron>
      <b-row>
        <b-col>
          <h3>
            <strong>Username:</strong>
            {{currentUser.username}}
          </h3>
          <br />
          <h3>
            {{currentUser.firstname}} {{currentUser.lastname}}
          </h3>
        </b-col>
        <b-col col lg="2">
          <avatar/>
        </b-col>
      </b-row>
      
      
    </b-jumbotron>
    <p>
      <strong>Token:</strong>
      {{currentUser.access_token.substring(0, 20)}} ... {{currentUser.access_token.substr(currentUser.access_token.length - 20)}}
    </p>
    <p>
      <strong>Id:</strong>
      {{currentUser.user_id}}
    </p>
    <p>
      <strong>Email:</strong>
      {{currentUser.email}}
    </p>
    <b-button @click="logout()" variant="outline-info" class="mb-2">
      <b-icon icon="power" aria-hidden="true"></b-icon> Logout
    </b-button>
    <b-button v-b-modal.edit-profile variant="outline-info" class="mb-2">
      <b-icon icon="pencil-square" aria-hidden="true"></b-icon> Edit Profile
    </b-button>

    <!-- Modal -->
    <b-modal id="edit-profile" title="Edit Profile" ok-title="Save" @ok="handleOk">
      <b-form @submit.stop.prevent="onSubmit" ref="form" v-if="show">
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
          label="Username:"
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
          label="Email:"
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

        </b-form>
    </b-modal>
    <label class="switch">
      <input id="themeToggle" type="checkbox" @click="toggleTheme()">
      <span class="slider round"></span>
    </label>

    <br />
    <app-color-picker class="column"/>
    <br />
     <themed-title>Examples of Themed Components</themed-title>
     <themed-btn>Themed Button</themed-btn>
  </div>
</template>

<script>
import Avatar from '@/components/Avatar';
import AppColorPicker from '@/components/AppColorPicker';
import { mapMutations } from 'vuex';
export default {
  name: 'Profile',
  components: {
       'Avatar': Avatar,
       'AppColorPicker': AppColorPicker
   },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    currentTheme() {
      return this.$store.state.theme;
    }
  },
  mounted() {
    if (this.currentTheme == 'light'){
      this.checked = false;
    } else {
      this.checked = true;
    }

    if (this.currentTheme == 'light') {
        document.getElementById("themeToggle").checked = false;
    } else {
        document.getElementById("themeToggle").checked = true;
    }

    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
  data() {
    return {
      selectedTheme: '',
      checked: null,
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
  methods: {
    ...mapMutations([
      'toggleTheme'
    ]),
    logout() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
    editProfile() {
      this.$router.push('/editProfile');
    },
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
          // Hide the modal manually
          this.$nextTick(() => {
            this.$bvModal.hide('edit-profile')
          })
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
    handleOk(bvModalEvt) {
        // Prevent modal from closing
        bvModalEvt.preventDefault()
        // Trigger submit handler
        this.onSubmit()
    }
  }
};
</script>