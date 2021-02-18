<template>
  <b-container class="search-card">
    <b-card>
      <b-row> {{ searchResult.firstname }} {{ searchResult.lastname }} </b-row>
      <b-row>
        <router-link :to="profileLink" exact>{{
          searchResult.username
        }}</router-link>
      </b-row>
    </b-card>
  </b-container>
</template>

<script>
export default {
  name: "SearchCard",
  props: {
    searchResult: {
      type: Object,
    },
  },
  computed: {
    profileLink() {
      return "/u/" + this.searchResult.username;
    },
  },
};
</script>

<style scoped>
.search-card {
  padding-bottom: 10px;
}
</style>