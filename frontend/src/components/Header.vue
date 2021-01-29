<template>
  <div id="header">
    <div id="headerContent">
      <b-row>
        <b-col cols="2">
          Logo Here
        </b-col>
        <b-col cols="8" style="text-align: center;">
          <h1>I am the header</h1>
        </b-col>
        <b-col cols="2">
          <h1>Maybe user stuff should go here</h1>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
export default {
    name: 'Header'
}
</script>

<style scoped>
#header {
  height: 60px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--app-color);
}

#headerContent {
  /* display: flex;
  flex-direction: column; */
  margin-left: 10px;
  width: 100%;
}
</style>