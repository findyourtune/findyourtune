<template>
  <div id="app">
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
// import Courses from './components/Courses.vue'

export default {
  name: 'App',
  // components: {
  //   Courses
  // }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  margin-top: 60px;
}
</style>
