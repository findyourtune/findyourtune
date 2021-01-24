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
    <b-button @click="editProfile()" variant="outline-info" class="mb-2">
      <b-icon icon="pencil-square" aria-hidden="true"></b-icon> Edit Profile
    </b-button>
  </div>
</template>

<script>
import Avatar from '@/components/Avatar';
export default {
  name: 'Profile',
  components: {
       'Avatar': Avatar
   },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    },
    editProfile() {
      this.$router.push('/editProfile');
    }
  }
};
</script>