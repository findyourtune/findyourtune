<template>
    <b-modal
      id="embed-spotify"
      hide-footer
      scrollable 
    >
    <template #modal-title>
      <b-input-group>
        <b-form-input
        autofocus
        v-model="searchString" 
        placeholder="Search..."
        ></b-form-input>
        <b-input-group-append is-text>
          <b-icon :disabled="!searchString.length" class="default-button" @click="getSearch()" icon="search"></b-icon>
        </b-input-group-append>
      </b-input-group>
    </template>
      <b-overlay :show="spotifyEmbedLoading" opacity="0.95" rounded="sm">
        <div v-if="!searchOccurred">
          <div v-for="(song, index) in suggestedTracks" :key="index">
            <div class="default-button">
                <song-card :song="song" @click.native="embedItem(song)"/>
            </div>
          </div>
        </div>
        <b-tabs v-if="searchOccurred" active class="overflow-tabs" content-class="mt-3" justified>
            <b-tab title="Tracks">
                <p v-if="music.songs.length == 0">Nothing here...</p>
                <div v-for="(song, index) in music.songs" :key="index">
                    <div class="default-button">
                        <song-card :song="song" @click.native="embedItem(song)"/>
                    </div>
                </div>
            </b-tab>
            <b-tab title="Albums">
                <p v-if="music.albums.length == 0">Nothing here...</p>
                <div v-for="(album, index) in music.albums" :key="index">
                    <div class="default-button">
                        <song-card :song="album" @click.native="embedItem(album)"/>
                    </div>
                </div>
            </b-tab>
            <b-tab title="Playlists">
                <p v-if="music.playlists.length == 0">Nothing here...</p>
                <div v-for="(playlist, index) in music.playlists" :key="index">
                    <div class="default-button">
                        <song-card :song="playlist" @click.native="embedItem(playlist)"/>
                    </div>
                </div>
            </b-tab>
            </b-tabs>
      </b-overlay>
    </b-modal>
</template>

<script>
import axios from 'axios';
import { mapMutations } from 'vuex';
import authHeader from '../services/auth/auth-header';
import SongCard from "./SongCard.vue";
import store from '../store';
export default {
  name: 'SpotifySearch',
  components: {
    SongCard
  },
  props: {
    suggestedTracks: {
      type: Array,
    }
  },
  data() {
    return {
      music: {
        songs: [],
        playlists: [],
        albums: []
      },
      searchString: '',
      spotifyEmbedLoading: false,
      searchOccurred: false
    };
  },
  mounted () {
    this.$root.$on('bv::modal::hide', () => {
        store.commit('pauseAudio') 
    })
  },
  methods: {
    ...mapMutations([
    'setAudio',
    'playAudio',
    'pauseAudio'
    ]),
    getSearch() {
        this.spotifyEmbedLoading = true;
        const path = this.$apiUrl + '/api/search/get_spotify_embed/' + this.searchString;
        axios.get(path, {
            headers: authHeader()
        })
        .then((res)=>{
            this.music = res.data;
            this.searchOccurred = true;
            this.spotifyEmbedLoading = false;
        })
        .catch((error)=>{
            console.error(error);
            this.searchResult = 'Could not load search'
        });
    },
    embedItem(item) {
        this.$emit('embed', item);

        // Reset modal if user was to press "Embed" again
        this.searchString = '';
        this.searchOccurred = false;

        this.$nextTick(() => {
            this.$bvModal.hide("embed-spotify");
        });
    }
  }
}
</script>