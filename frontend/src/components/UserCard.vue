<template>
  <b-container class="user-card">
    <b-row>
      <b-col cols="2" class="avatar-col">
        <b-avatar
          :style="{'background-color': appColor}"
          variant="info"
          :text="getAvatarText()"
          size="2.5rem"
        ></b-avatar>
      </b-col>
      <b-col class="name-col">
        {{ user.user_firstname }} {{ user.user_lastname }}
      </b-col>
      <b-col cols="3" class="fxn-col">
        <b-button
          size="sm"
          v-if="
            user.username != currentUser.username && !user.user_followed && showFxns
          "
          @click="followUser()"
          pill
          class="m-1 custom-btn"
          >Follow</b-button
        >
        <b-button
          size="sm"
          v-if="
            user.username != currentUser.username && user.user_followed && showFxns
          "
          @click="unfollowUser()"
          pill
          class="m-1 custom-btn"
          >Unfollow</b-button
        >
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import axios from "axios";
import authHeader from "../services/auth/auth-header";
export default {
  name: "UserCard",
  props: {
    user: {
      type: Object,
    },
    currentUser: {
      type: Object
    },
    index: {
      type: Number
    },
    showFxns: {
      Type: Boolean
    }
  },
  data() {
    return {
      appColor: ''
    }
  },
  mounted() {
    this.appColor = this.user.user_appcolor ? this.user.user_appcolor : this.$store.state.defaultAppColor;
  },
  methods: {
    followUser() {
      const path = "http://localhost/api/social/follow_user";
      const data = {
        follower_username: this.currentUser.username,
        followed_username: this.user.user_username,
      };
      axios
        .post(path, data, {
          headers: authHeader(),
        })
        .then(() => {
          this.user.user_followed = true;
        })
        .catch((error) => {
          console.error("Could not follow user", error);
        });
    },
    unfollowUser() {
      const path = "http://localhost/api/social/unfollow_user";
      const data = {
        follower_username: this.currentUser.username,
        followed_username: this.user.user_username,
      };
      axios
        .post(path, data, {
          headers: authHeader(),
        })
        .then(() => {
          this.user.user_followed = false;
          // this.$router.go();
        })
        .catch((error) => {
          console.error("Could not unfollow user", error);
        });
    },
    getAvatarText() {
      try {
        let firstInitial = this.user.user_firstname.charAt(0);
        let lastInitial = this.user.user_lastname.charAt(0);
        return firstInitial.toUpperCase() + lastInitial.toUpperCase();
      } catch (err) {
        return "";
      }
    },
  },
};
</script>

<style>
.user-card {
  padding-bottom: 10px;
}
.user-card > div {
  margin-right: 15px !important;
  align-items: center;
}
.name-col {
  text-align: left;
}
.col-2 {
  padding-right: 0px !important;
  flex: 0 0 10% !important;
  max-width: 10% !important;
}
</style>