<template>
  <div id="app" :style="cssProps">
    <Header></Header>
    <div class="page">
      <SideBarLeft></SideBarLeft>
      <div class="main">
        <div class="sub-main">
          <div class="main-content">
            <router-view></router-view>
          </div>  
          <SideBarRight></SideBarRight>
        </div>
      </div>
    </div>
  </div>
</template>

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
}

.page {
  display: flex;
  height: calc( 100vh - 60px);
  overflow-x: hidden;
}

.main {
  background-color: var(--bg);
  overflow-y: auto;
  align-items: flex-start;
  flex-shrink: 1;
  flex-grow: 1;
  flex-basis: auto;
  display: flex;
  flex-direction: column;
}

.sub-main {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  flex-basis: auto;
  width: 100%;
  flex-shrink: 1;
  flex-grow: 1;
}

.main-content {
  width: 800px;
  flex-basis: auto;
  flex-shrink: 0; 
  padding: 10px 15px;
  flex-grow: 1;
  margin: 0 auto;
  position: relative;
}

/* When screen gets smaller, hide "Suggested Content" */
@media print, screen and (max-width: 1000px) {
  .main-content {
      width: auto;
  }
}
</style>
