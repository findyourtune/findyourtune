<template>
  <div class="sideBarLeft">
    <div class="sideBarLeftContent">
      <div class="routes">
        <div>
          <router-link to="/" exact>Home</router-link>
        </div>
        <div>
          <router-link to="/courses" exact>About</router-link>
        </div>
        <div>
          <router-link to="/login" exact>Log In</router-link>
        </div>
        <div>
          <router-link to="/register" exact>Register</router-link>
        </div>
        <div>
          <router-link to="/profile" exact>Profile</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    name: 'SideBarLeft'
}
</script>

<style scoped>
.sideBarLeft {
  max-width: 400px;
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