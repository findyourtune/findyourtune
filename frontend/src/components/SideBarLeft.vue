<template>
  <div id="side-bar-left">
    <ul>
      <li>
        <router-link to="/" exact>Home</router-link>
      </li>
      <li>
        <router-link to="/courses" exact>About</router-link>
      </li>
      <li>
        <router-link to="/login" exact>Log In</router-link>
      </li>
      <li>
        <router-link to="/register" exact>Register</router-link>
      </li>
      <li>
        <router-link to="/profile" exact>Profile</router-link>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
    name: 'SideBarLeft'
}
</script>

}

<style scoped>
#side-bar-left{
  margin-top: 100px;
  padding: 0;
  width: 200px;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
}
router-link{
  display: block;
  color: black;
  padding: 16px;
  text-decoration: none;
}
</style>