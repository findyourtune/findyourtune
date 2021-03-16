<template>
  <b-container class="suggested-people-card">
    <b-card>
      <b-row>
        <b-col>
          <div @click="goToUser()" class="user-page-link-button">
            <b-avatar
              :style="{ 'background-color': appColor }"
              variant="info"
              :text="getAvatarText()"
              size="3.5rem"
            ></b-avatar>
            <span class="user-info">
              <div class="user-display-name">
                {{ person.user_firstname }} {{ person.user_lastname }}
              </div>
              <div class="user-username">@{{ person.user_username }}</div>
            </span>
          </div>
        </b-col>
      </b-row>
    </b-card>
  </b-container>
</template>

<script>
export default {
  name: "SuggestedPeople",
  props: {
    person: {
      type: Object,
    },
  },
  computed: {
    profileLink() {
      return "/u/" + this.person.user_username;
    },
  },
  methods: {
    getAvatarText() {
      try {
        let firstInitial = this.person.user_firstname.charAt(0);
        let lastInitial = this.person.user_lastname.charAt(0);
        return firstInitial.toUpperCase() + lastInitial.toUpperCase();
      } catch (err) {
        return "";
      }
    },
    goToUser() {
      this.$router.push(this.profileLink);
    },
  },
};
</script>

<style scoped>
.suggested-people-card {
  padding-bottom: 10px;
}

.user-info {
    vertical-align: middle;
    display: inline-block;
    padding-left: 15px;
}
.user-display-name {
    font-size: 1.2rem;
    font-style: bold;
    display: inline-block;
}
.user-username {
    font-size: 14px;
    font-style: italic;
}
</style>