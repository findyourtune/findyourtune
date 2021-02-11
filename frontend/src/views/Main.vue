<template>
  <div class="timeline">
    <div :class="$options.name">
      <div :class="`${$options.name}__messageBox`">
        <tweet-box v-model="tweet" />
      </div>
    </div>
    <div id="postbutton">
      <b-button pill variant="success" v-on:click="postPost">Post</b-button>
    </div>
    <div
      v-for="(item, i) in posts"
      v-bind:key="i"
    >
      <div class="content">
        <h2>{{item.name}}</h2>
        <h4>{{item.text}}</h4>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '../services/auth/auth-header';
import TweetBox from '../components/Tweetbox.vue';
export default {
  name: 'Main',
  components: {
    TweetBox,
  },
  data() {
    return {
      tweet: ``,
      posts: {},
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    getPosts() {
      const path = 'http://localhost/api/post';
      axios.get(path, {
        headers: authHeader()
      })
      .then((res)=>{
        this.posts = res.data
      })
      .catch((error)=>{
        console.error(error);
        this.post = 'Could not load posts'
      });
    },
    postPost() {
      const path = 'http://localhost/api/post';
      const data = { username: this.userInfo.username, text: this.tweet, spotify_data: null}
      axios.post(path, data, {
        headers: authHeader()
      })
      .catch(error => {
        console.error("Could not POST user post", error);
      })
      this.getPosts();
    },
    updateValue(e) {
      this.$emit('input', e.target.value);
    },
    getUserInfo() {
      const path = 'http://localhost/api/auth/get_user_info';
      var userInfo = this.currentUser ? this.currentUser : ''
      axios.get(path, {
        params: {
          access_token: userInfo.access_token ? userInfo.access_token : ''
        },
        headers: authHeader()
      })
      .then((res) => {
        this.userInfo = res.data.userInfo ? res.data.userInfo : res.data.status
      })
      .catch((error) => {
        console.error(error);
        this.userInfo = 'User not logged in'
      });
    },
  },
  created() {
    this.getUserInfo();
    this.getPosts();
  },
}
</script>

<style lang="scss">
@import '~normalize.css';
@import '~reset-css/sass/_reset.scss';
* {
  box-sizing: border-box;
}
html body {
  color: #444;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}
.App {
  &__messageBox {
    padding: 1em;
    background-color: #e5f6f8;
  }
}
</style>