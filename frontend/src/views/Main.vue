<template>
  <div class="timeline">
    <div>
      <b-container>
        <b-card class="newpost-card">
          <b-row class="inputRow">
            <b-form-input v-model="message" placeholder="What's Happening?"></b-form-input>
          </b-row>
          <b-row v-if="embeddedSong.name" class="embedRow">
            <b-col cols="2"></b-col>
            <b-col class="content-embed">
              <div class="sub-content-embed">
                <div class="image-embed">
                  <img :src="getItemImage()"> 
                </div>
                <div class="info-embed">
                  <div>{{embeddedSong.name}}</div>
                  <p class="artist-name">{{embeddedSong.artist.name}}</p>
                </div>
              </div>
            </b-col>
            <b-col cols="2">
              <span class="remove-embed"><b-icon v-b-tooltip.hover.bottom="'Remove Embed'" class="delete-btn" @click="removeEmbed()" icon="x-circle"></b-icon></span>
            </b-col>
          </b-row>
          <b-row class="buttonRow">
            <b-col>
              <p v-if="currentUser.spotify_linked" p class="h5"><b-icon  v-b-tooltip.hover.bottom="'Embed Spotify'" class="default-button" @click="getSpotifyEmbedPayload()" v-b-modal.embed-spotify icon="music-note-list"></b-icon></p>
            </b-col>
            <b-col class="buttonCol">
              <b-button pill class="custom-btn-filled" v-on:click="postPost" :disabled="!message.length">Post</b-button>
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
    <spotify-search :suggestedTracks="suggestedTracks" @embed="onEmbed"/>
  </div>
</template>

<script>
import axios from 'axios';
import authHeader from '../services/auth/auth-header';
import PostCard from '../components/PostCard.vue';
import SpotifySearch from '../components/SpotifySearch.vue';
export default {
  name: 'Main',
  components: {
    PostCard,
    SpotifySearch
  },
  data() {
    return {
      show: true,
      message: '',
      posts: {},
      suggestedTracks: [],
      embeddedSong: {}
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
      });
    },
    postPost() {
      const path = this.$apiUrl + '/api/social/post';
      const data = { 
        user_id: this.currentUser.user_id, 
        text: this.message, 
        spotify_data: this.getSpotifyData()
      }
      axios.post(path, data, {
        headers: authHeader()
      })
      .then(()=> {
        this.$router.go()
      })
      .catch(error => {
        console.error("Could not POST user post", error);
      })
      
    },
    getSpotifyEmbedPayload() {
      const path = this.$apiUrl + '/api/music/get_short_term_music';
      axios.get(path, {
        headers: authHeader()
      })
      .then((res)=>{
        this.suggestedTracks = res.data;
      })
      .catch((error)=>{
        console.error(error);
      });
    },
    onEmbed(item) {
      this.embeddedSong = item;
    },
    getSpotifyData() {
      if (this.embeddedSong.name) {
        return this.embeddedSong.item_id + ',' + this.embeddedSong.item_type + ',' + this.embeddedSong.name + ',' + this.embeddedSong.artist.name + ',' + this.getItemImage();
      } else{
        return null;
      }
    },
    getItemImage() {
        try {
            return this.embeddedSong.images[1].url;
        } catch (err) {
            return this.embeddedSong.images[0].url;
        }
    },
    removeEmbed() {
        this.embeddedSong = {};
    }
  },
  created() {
    this.getPosts();
  },
}
</script>

<style>
  .buttonRow {
    padding-top: 10px;
    align-items: flex-end;
    padding-left: 15px;
  }
  .buttonCol {
    text-align: right;
  }
  .newpost-card > div {
    padding-bottom: .5em !important;
  }
  .remove-embed {
    float: right;
    padding-top: 15px;
  }
</style>