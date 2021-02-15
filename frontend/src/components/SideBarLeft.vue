<template>
  <div class="sideBarLeft">
    <div class="sideBarLeftContent">
      <div class="routes">
        <div>
          <router-link to="/" exact>Home</router-link>
        </div>
        <div v-if="loggedIn">
          <router-link to="/courses" exact>Messages</router-link>
        </div>
        <div v-if="!loggedIn">
          <router-link to="/login" exact>Log In</router-link>
        </div>
        <div v-if="!loggedIn">
          <router-link to="/register" exact>Register</router-link>
        </div>
        <div v-if="loggedIn">
          <router-link :to=profileLink exact>Profile</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'SideBarLeft',
    computed: {
      currentUser() {
        return this.$store.state.auth.user;
      },
      loggedIn() {
        return this.$store.state.auth.status.loggedIn;
      },
      profileLink() {
        return '/u/' + this.$store.state.auth.user.username;
      }
    },
}
</script>

<style scoped>
.sideBarLeft {
  max-width: 500px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  flex-basis: 0;
  flex-shrink: 0;
  -webkit-box-align: end;
  align-items: flex-end;
  border-right: 1px solid var(--app-color);
}

.sideBarLeftContent {
  padding-top: 10px;
  display: flex;
  width: 200px;
  padding-left: 10px;
  padding-right: 10px;
}

.routes {
  display: flex;
  flex-direction: column;
}

.routes > div{
  display: flex;
  text-decoration: none;
  width: 100%;
  padding-bottom: 7px;
  padding-top: 7px;
}
</style>