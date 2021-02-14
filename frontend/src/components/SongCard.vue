<template>
  <b-container class="song-card">
      <b-card>
        <b-row>
            <b-col>
                <img class="artist-img" :src="song.images[2].url"> 
            </b-col>
            <b-col>
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
};
</script>

<style>
.artist-img {
    width: 64px;
}

.song-card {
    padding-bottom: 10px;
}
</style>