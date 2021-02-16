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
    <b-overlay :show="userPostsLoading" opacity="0.95" rounded="sm">
      <div v-for="(post, index) in posts" :key="index">
        <post-card :post="post"/>
      </div>
    </b-overlay>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '../services/auth/auth-header';
import TweetBox from '../components/Tweetbox.vue';
import PostCard from '../components/PostCard.vue';
export default {
  name: 'Main',
  components: {
    TweetBox,
    PostCard
  },
  data() {
    return {
      tweet: '',
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
      this.userPostsLoading = true;
      const path = 'http://localhost/api/social/get_posts';
      axios.get(path, {
        headers: authHeader()
      })
      .then((res)=>{
        this.posts = res.data;
        this.userPostsLoading = false;
      })
      .catch((error)=>{
        console.error(error);
        this.post = 'Could not load posts'
      });
    },
    postPost() {
      const path = 'http://localhost/api/social/post';
      const data = { username: this.currentUser.username, text: this.tweet, spotify_data: null}
      axios.post(path, data, {
        headers: authHeader()
      })
      .then(()=> {
        this.getPosts();
      })
      .catch(error => {
        console.error("Could not POST user post", error);
      })
      
    },
    updateValue(e) {
      this.$emit('input', e.target.value);
    },
  },
  created() {
    this.getPosts();
  },
}
</script>