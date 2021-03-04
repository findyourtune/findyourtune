<template>
  <b-container class="song-card">
      <b-card>
        <b-row>
            <b-col cols="3">
                <img class="artist-img" :src="getItemImage()"> 
            </b-col>
            <b-col class="item-info">
                <div>{{song.name}}</div>
                <p class="artist-name">{{song.artist.name}}</p>
            </b-col>           
        </b-row>
      </b-card>
  </b-container>
</template>

<script>
export default {
    name: 'SongCard',
    props: {
        song: {
            type: Object
        }  
    },
    methods: {
        getItemImage() {
            try {
                return this.song.images[2].url;
            } catch (err) {
                return this.song.images[0].url;
            }
        }
    }
};
</script>

<style>
.artist-img {
    width: 64px;
}
.song-card {
    padding-bottom: 10px;
}
.item-info {
    white-space: break-spaces;
}
</style>