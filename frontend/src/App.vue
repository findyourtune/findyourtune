<template>
    <div id="app" :style="cssProps">
      <div class="container">
        <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
        <div>
          <router-link to="/" exact>Home</router-link>
          <router-link to="/courses" exact>About</router-link>
          <router-link to="/login" exact>Log In</router-link>
          <router-link to="/register" exact>Register</router-link>
          <router-link to="/profile" exact>Profile</router-link>
        </div>
        <router-view></router-view>
      </div>
    </div>
</template>

// This is what I have in mind for root skeleton, the router-links above will moved to the SideBar component
// <div id="app">
//    <HeaderBar></HeaderBar>
//    <SideBarLeft></SideBarLeft>
//    <SideBarRight></SideBarRight>
//    <main class="view">
//      <router-view></router-view>
//    </main>
//   </div>

<script>
export default {
  name: 'App',
  computed: {
    cssProps() {
      return {
        '--app-color': (this.$store.state.appColor)
      }
    }
  }
}
</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: "Gill Sans", "Gill Sans MT", Calibri, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
}
</style>
