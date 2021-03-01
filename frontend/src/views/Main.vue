<template>
  <div class="timeline">
    <div>
      <b-container class="newpost-card">
        <b-card>
          <b-row class="inputRow">
            <b-form-input v-model="message" placeholder="What's Happening?"></b-form-input>
          </b-row>
          <b-row class="buttonRow">
            <b-col class="buttonCol">
              <b-button pill variant="info" v-on:click="postPost">Post</b-button>
            </b-col>
          </b-row>
        </b-card>
      </b-container>
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
import PostCard from '../components/PostCard.vue';
export default {
  name: 'Main',
  components: {
    PostCard
  },
  data() {
    return {
      message: '',
      posts: {},
    };
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    messageState() {
      return this.message.length > 140 ? false : true
    }
  },
  methods: {
    getPosts() {
      this.userPostsLoading = true;
      const path = this.$apiUrl + '/api/social/get_posts';
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
      const path = this.$apiUrl + '/api/social/post';
      const data = { username: this.currentUser.username, text: this.message, spotify_data: null}
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

<style>
  .buttonRow {
    padding-top: 10px;
  }
  .buttonCol {
    text-align: right;
  }
</style>