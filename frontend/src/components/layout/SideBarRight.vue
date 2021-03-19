<template>
  <div class="sideBarRight">
    <div class="sideBarRightContent">
      <div v-if="loggedIn">
        <suggested />
      </div>
    </div>
  </div>
</template>

<script>
import Suggested from "./Suggested.vue";
export default {
  name: "SideBarRight",
  components: { Suggested },
  computed: {
    loggedIn() {
      return this.$store.state.auth.status.loggedIn;
    },
  },
};
</script>


<style scoped>
.sideBarRight {
  /* width: 450px; */
  display: flex;
  flex-direction: column;
  -webkit-box-align: start;
  align-items: flex-start;
  border-left: 1px solid var(--app-color);
  flex-grow: 2;
  flex-basis: 0;
  flex-shrink: 0;
}

.sideBarRightContent {
  padding-top: 10px;
  display: flex;
  width: 250px;
  padding-left: 10px;
  padding-right: 10px;
}

@media print, screen and (max-width: 1000px) {
  .sideBarRight {
    display: none;
  }
}
</style>
