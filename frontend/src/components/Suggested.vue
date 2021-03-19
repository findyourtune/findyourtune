<template>
  <div>
    <b-container>
      <b-row class="display-name">
        <span>Suggested People</span>
      </b-row>
      <b-row>
        <b-overlay :show="suggestPeopleLoading" opacity="0.95" rounded="sm">
          <div v-for="(person, index) in suggestPeopleResults" :key="index">
            <suggested-people :person="person" />
          </div>
        </b-overlay>
      </b-row>
    </b-container>
    <b-container>
      <b-row class="display-name">
        <span>Suggested Music</span>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import SuggestedPeople from "./SuggestedPeople.vue";
import authHeader from "../services/auth/auth-header";
export default {
  name: "Suggested",
  components: { SuggestedPeople },
  data() {
    return {
      suggestPeopleResults: [],
      suggestPeopleLoading: false,
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
  },
  created() {
    this.getSuggestedPeople();
  },
  methods: {
    getSuggestedPeople() {
      const path =
        this.$apiUrl +
        "/api/suggested/get_suggested_people/" +
        this.currentUser.username;
      this.suggestPeopleLoading = true;
      axios
        .get(path, {
          headers: authHeader(),
        })
        .then((res) => {
          this.suggestPeopleResults = res.data.people;
          this.suggestPeopleLoading = false;
        })
        .catch((error) => {
          console.error(error);
          //this.suggestPeopleResults = []
        });
      console.log("Suggested Music");
    },
    getSuggestedMusic() {
      console.log("Suggested Music");
    },
  },
};
</script>

<style scoped>
.display-name {
  padding: 10px;
}

.display-name > span {
  font-size: 1.5rem;
}
</style>