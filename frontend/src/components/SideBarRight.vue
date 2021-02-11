<template>
  <div class="sideBarRight">
    <div class="sideBarRightContent">
      <h1>Suggested Content</h1>
    </div>
  </div>
</template>

<script>
export default {
    name: 'SideBarRight'
}
</script>

}


<style scoped>
.sideBarRight {
  /* width: 450px; */
  display: flex;
  flex-direction: column;
  -webkit-box-align: start;
  align-items: flex-start;
  border-left: 1px solid var(--app-color);
  flex-grow: 3;
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
