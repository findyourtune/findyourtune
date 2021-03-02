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
      <b-tabs v-if="searchOccurred" content-class="mt-3" justified>
        <b-tab title="Users" active>
          <div v-for="(searchResult, index) in searchResults.users" :key="index">
            <search-card :searchResult="searchResult" />
          </div>
        </b-tab>
        <b-tab title="Music">
          <div v-for="(song, index2) in searchResults.music" :key="index2">
            <song-card :song="song" />
          </div>
        </b-tab>
      </b-tabs>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '../services/auth/auth-header';
import SearchCard from '../components/SearchCard.vue'
import SongCard from '../components/SongCard.vue';
export default {
  name: "Search",
  components:{
    SearchCard,
    SongCard
  },
  data() {
    return {
      searchString: '',
      searchStringPrev: '',
      searchResults: {
        users: [],
        music: []
      },
      searchLoading: false,
      searchOccurred: false
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
        this.searchOccurred = true;
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