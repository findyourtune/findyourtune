<template>
  <div id="app" :style="cssProps">
    <div >
      <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
      <Header></Header>
      <side-bar-left></side-bar-left>
      <div id="main-content">
        <router-view></router-view>
      </div>
      <side-bar-right></side-bar-right>
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
import Header from './components/Header.vue';
import SideBarLeft from "./components/SideBarLeft.vue";
import SideBarRight from "./components/SideBarRight.vue";

export default {
  name: "App",
  computed: {
    cssProps() {
      return {
        '--app-color': (this.$store.state.appColor)
      }
    }
  },
  components: {
    Header,
    SideBarLeft,
    SideBarRight
  },
};
</script>

<style>
#app {
  /* font-family: Avenir, Helvetica, Arial, sans-serif; */
  font-family: "Gill Sans", "Gill Sans MT", Calibri, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  /* text-align: center; */
  color: #2c3e50;
}

#main-content{
  position: fixed;
  width: 80%;
  margin-top: 100px;
  margin-left: 200px;
  padding: 16px 10px;
}
</style>
