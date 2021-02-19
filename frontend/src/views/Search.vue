<template>
  <div>
    <input v-model="searchString" placeholder="Search.." />
    <b-button
      pill
      :disabled="!searchString.length || searchString === searchStringPrev"
      class="m-2 custom-btn"
      @click="getSearch()"
      >Search</b-button
    >
    <b-overlay :show="searchLoading" opacity="0.95" rounded="sm">
      <div v-for="(searchResult, index) in searchResults" :key="index">
        <search-card :searchResult="searchResult" />
      </div>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '../services/auth/auth-header';
import SearchCard from '../components/SearchCard.vue'
export default {
  name: "Search",
  components:{
    SearchCard
  },
  data() {
    return {
      searchString: '',
      searchStringPrev: '',
      searchResults: {}
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    getSearch() {
      this.searchStringPrev = this.searchString;
      this.searchLoading = true;
      const path = this.$apiUrl + '/api/search/search_users/' + this.searchString;
      axios.get(path, {
        headers: authHeader()
      })
      .then((res)=>{
        this.searchResults = res.data;
        this.searchLoading = false;
      })
      .catch((error)=>{
        console.error(error);
        this.searchResult = 'Could not load search'
      });
    },
  },
};
</script>

<style scoped>
</style>