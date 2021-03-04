<template>
  <b-container class="post-card">
      <b-card>
        <b-row>
            <b-col>
                <div @click="goToUser()" class="user-page-link-button">
                    <b-avatar
                        :style="{'background-color': appColor}"
                        variant="info"
                        :text="getAvatarText()"
                        size="3.5rem"
                    ></b-avatar>
                    <span class="user-info">
                        <div class="user-display-name">
                            {{ post.name }}
                        </div><span class="timestamp" v-b-tooltip.hover.right="timeStampTooltip"> &#8226; {{timestampDisplay}}</span>
                        <div class="user-username">@{{
                            post.username
                        }}</div>
                    </span>
                </div>        
            </b-col>
            <b-col cols="3" class="function-col">
                <span v-if="currentUser && post.user_id == currentUser.user_id">
                    <b-icon class="delete-btn" @click="deletePost()" icon="trash"></b-icon>
                </span>
                <span v-if="currentUser && post.user_id != currentUser.user_id">
                    <b-icon v-if="!post.current_user_likes" class="like-btn-fill" @click="toggleLikePost()" icon="heart"></b-icon>
                    <b-icon v-if="post.current_user_likes" class="like-btn" @click="toggleLikePost()" icon="heart-fill"></b-icon>
                </span>
                <span>
                    <b-icon class="default-button" @click="postComment()" icon="arrow-return-left"></b-icon>
                </span>
            </b-col>
        </b-row>
        <b-row class="post-area">
            {{post.text}}
        </b-row>
        <b-row v-if="post.spotify_data != null" class="embedRow">
            <b-col cols="2"></b-col>
            <b-col class="content-embed">
              <div class="sub-content-embed default-button" @click="openSpotifyLink(embeddedItem.url)">
                <div class="image-embed">
                  <img :src="embeddedItem.imageUrl"> 
                </div>
                <div class="info-embed">
                  <div>{{embeddedItem.name}}</div>
                  <p class="artist-name">{{embeddedItem.artist}}</p>
                </div>
              </div>
            </b-col>
            <b-col cols="2"></b-col>
        </b-row>
      </b-card>
  </b-container>
</template>

<script>
import axios from "axios";
import authHeader from "../services/auth/auth-header";
export default {
    name: 'PostCard',
    props: {
        post: {
            type: Object
        }  
    },
    data: function () {
        return {
            appColor: '',
            timestampDisplay: '',
            timeStampTooltip: '',
            embeddedItem: {
                id: '',
                type: '',
                name: '',
                artist: '',
                imageUrl: '',
                url: ''
            },
        }
    },
    created() {
        this.getPostTimeStamp();
    },
    mounted() {
        this.appColor = this.post.appColor ? this.post.appColor : this.$store.state.defaultAppColor;
        this.timeStampTooltip = this.$moment(this.post.timestamp).format("h:mm A - MMM D, YYYY");

        if (this.post.spotify_data != null) {
            var dataArray = this.post.spotify_data.split(',');
            this.embeddedItem.id = dataArray[0];
            this.embeddedItem.type = dataArray[1];
            this.embeddedItem.name = dataArray[2];
            this.embeddedItem.artist = dataArray[3];
            this.embeddedItem.imageUrl = dataArray[4];
            this.embeddedItem.url = this.$spotifyUrl + dataArray[1] + '/' + dataArray[0];
        }
    },
    computed: {
        currentUser() {
            return this.$store.state.auth.user;
        },
        profileLink() {
            return "/u/" + this.post.username;
        }
    },
    methods: {
        toggleLikePost() {
            if (!this.currentUser) {
                this.$router.push("/login");
            } else {
                const path = this.$apiUrl + "/api/social/toggle_like_post";
                const data = {
                    post_id: this.post.post_id,
                    user_id: this.currentUser.user_id,
                    post_user_id: this.post.user_id
                };
                axios
                    .post(path, data, {
                        headers: authHeader(),
                    })
                    .then((res) => {
                        this.post.current_user_likes = res.data.like;
                    })
                    .catch((error) => {
                    console.error("Could not toggle like", error);
                });
            }
        },
        deletePost() {
            if (!this.currentUser) {
                this.$router.push("/login");
            } else {
                this.$bvModal.msgBoxConfirm('Are you sure you would like to delete this post?', {
                    okTitle: 'Delete',
                    okVariant: 'danger',
                    centered: true
                })
                .then(value => {
                    if (value == true) {
                        const path = this.$apiUrl + "/api/social/delete_post";
                        const data = {
                            post_id: this.post.post_id,
                            user_id: this.currentUser.user_id
                        };
                        axios
                            .post(path, data, {
                                headers: authHeader(),
                            })
                            .then(() => {
                                this.$router.go();
                            })
                            .catch((error) => {
                            console.error("Could not delete post", error);
                        });
                    }
                })
                .catch(err => {
                    console.error(err);
                })
            }
        },
        getPostTimeStamp() {
            var postTimeStamp = this.$moment(this.post.timestamp);
            var currentTime = this.$moment();
            var diff = currentTime.diff(postTimeStamp, 'hours');
            if (diff > 24) {
                diff = currentTime.diff(postTimeStamp, 'days');
                this.timestampDisplay = diff + 'd'
                if (diff > 7) {
                    this.timestampDisplay = this.$moment(this.post.timestamp).format("MMM D, YYYY");
                }
            } else if (diff < 1) {
                diff = currentTime.diff(postTimeStamp, 'minutes');
                this.timestampDisplay = diff + 'm'
            } else {
                this.timestampDisplay = diff + 'h'
            }
        },
        goToUser() {
            this.$router.push(this.profileLink);
        },
        getItemImage() {
            try {
                return this.song.images[2].url;
            } catch (err) {
                return this.song.images[0].url;
            }
        },
        getAvatarText() {
            try {
                let firstInitial = this.post.firstname.charAt(0);
                let lastInitial = this.post.lastname.charAt(0);
                return firstInitial.toUpperCase() + lastInitial.toUpperCase();
            } catch (err) {
                return "";
            }
        },
        openSpotifyLink(url) {
            window.open(url);
        }
    }
};
</script>

<style>
.post-card {
    padding-top: 10px;
}
.function-col {
    text-align: right;
}
.function-col > span {
    padding-left: 15px;
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
.post-area {
    padding: 10px;
    padding-bottom: 0;
}
</style>