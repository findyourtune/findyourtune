<template>
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
</template>

<script>
export default {
    name: 'NewPostCard',
    props: {
        post: {
            type: Object
        }  
    },
    methods: {
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
      }
    }
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