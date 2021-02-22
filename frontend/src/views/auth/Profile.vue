<template>
  <div>
    <b-container fluid>
      <b-overlay :show="userProfileLoading" opacity="0.95" rounded="sm">
        <b-card>
          <b-container fluid>
            <b-row class="avatar-row">
              <b-col>
                <b-avatar
									size="6rem"
									id="user-avatar"
                  variant="info"
                  :text="getAvatarText()"
                ></b-avatar>
              </b-col>
              <b-col class="edit-profile">
                <b-button
                  v-if="
                    !user.spotify_linked &&
                    user.username == currentUser.username
                  "
                  v-b-modal.edit-spotify-account
                  pill
                  class="m-2 custom-btn"
                  >Link Spotify</b-button
                >
                <b-button
                  v-if="user.username == currentUser.username"
                  v-b-modal.edit-profile
                  pill
                  class="m-2 custom-btn"
                  >Edit Profile</b-button
                >
                <b-button
                  v-if="
                    user.username != currentUser.username && !user.user_followed
                  "
                  @click="followUser()"
                  pill
                  class="m-2 custom-btn"
                  >Follow</b-button
                >
                <b-button
                  v-if="
                    user.username != currentUser.username && user.user_followed
                  "
                  @click="unfollowUser()"
                  pill
                  class="m-2 custom-btn"
                  >Unfollow</b-button
                >
              </b-col>
            </b-row>

            <b-row>
              <b-col>
                <b-row class="display-name">
                  <span>{{ user.firstname }} {{ user.lastname }}</span>
                </b-row>

                <b-row class="username" v-if="user.username">
                  <span>@{{ user.username }}</span>
                </b-row>

                <b-row class="bio" v-if="user.bio">
                  <p>
                    {{ user.bio }}
                  </p>
                </b-row>
              </b-col>
              <b-col class="follow-counts">
                <div v-b-modal.view-followers @click="getFollowRels(0)">
                  <b>{{ user.following_count }}</b> <span>Following</span>
                </div>
                <div v-b-modal.view-followers @click="getFollowRels(1)">
                  <b>{{ user.follower_count }}</b> <span>Followers</span>
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-overlay>
    </b-container>

    <themed-divider></themed-divider>

    <b-tabs content-class="mt-3" justified class="profile-tabs">
      <b-tab title="Posts" active>
        <b-overlay :show="userPostsLoading" opacity="0.95" rounded="sm">
          <div v-for="(post, index) in posts" :key="index">
            <post-card :post="post" />
          </div>
        </b-overlay>
      </b-tab>
      <b-tab title="Music">
        <p v-if="user.spotify_linked">Showing short-term top tracks</p>
        <p v-if="!user.spotify_linked">This user is not connected to Spotify</p>
        <div v-for="(song, index) in songs" :key="index">
          <song-card :song="song" />
        </div>
      </b-tab>
    </b-tabs>

    <!-- Modal -->
    <b-modal
      id="edit-profile"
      title="Edit Profile"
      ok-title="Save"
      @ok="handleOk"
    >
      <b-form @submit.stop.prevent="onSubmit" ref="form" v-if="show">
        <b-row>
          <b-col>
            <b-form-group
              id="input-group-1"
              label="First Name"
              label-for="input-1"
            >
              <b-form-input
                autocomplete="off"
                id="input-1"
                name="input-1"
                v-model="form.firstname"
                type="text"
                placeholder="Enter first name"
                v-validate="{ required: true, min: 2 }"
                :state="validateState('input-1')"
                aria-describedby="input-1-live-feedback"
                data-vv-as="First Name"
              ></b-form-input>
              <b-form-invalid-feedback id="input-1-live-feedback">{{
                veeErrors.first("input-1")
              }}</b-form-invalid-feedback>
            </b-form-group>
          </b-col>
          <b-col>
            <b-form-group
              id="input-group-2"
              label="Last Name"
              label-for="input-2"
            >
              <b-form-input
                autocomplete="off"
                id="input-2"
                name="input-2"
                v-model="form.lastname"
                type="text"
                placeholder="Enter last name"
                v-validate="{ required: true, min: 2 }"
                :state="validateState('input-2')"
                aria-describedby="input-2-live-feedback"
                data-vv-as="Last Name"
              ></b-form-input>
              <b-form-invalid-feedback id="input-2-live-feedback">{{
                veeErrors.first("input-2")
              }}</b-form-invalid-feedback>
            </b-form-group>
          </b-col>
        </b-row>

        <b-form-group id="input-group-3" label="Username" label-for="input-3">
          <b-form-input
            autocomplete="off"
            id="input-3"
            name="input-3"
            v-model="form.username"
            type="text"
            placeholder="Enter username"
            v-validate="{ required: true, min: 8 }"
            :state="validateState('input-3')"
            aria-describedby="input-3-live-feedback"
            data-vv-as="Username"
          ></b-form-input>
          <b-form-invalid-feedback id="input-3-live-feedback">{{
            veeErrors.first("input-3")
          }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group id="input-group-4" label="Email" label-for="input-4">
          <b-form-input
            autocomplete="off"
            id="input-4"
            name="input-4"
            v-model="form.email"
            type="email"
            placeholder="Enter email"
            v-validate="{ required: true, min: 5 }"
            :state="validateState('input-4')"
            aria-describedby="input-4-live-feedback"
            data-vv-as="Email"
          ></b-form-input>
          <b-form-invalid-feedback id="input-4-live-feedback">{{
            veeErrors.first("input-4")
          }}</b-form-invalid-feedback>
        </b-form-group>

        <b-form-group id="input-group-5" label="Bio" label-for="input-5">
          <b-form-textarea
            id="input-5"
            name="input-5"
            placeholder="Enter something about yourself..."
            rows="3"
            v-model="form.bio"
            no-resize
            v-validate="{ max: 160 }"
            :state="validateState('input-5')"
            aria-describedby="input-5-live-feedback"
            data-vv-as="Bio"
          ></b-form-textarea>
          <b-form-invalid-feedback id="input-5-live-feedback">{{
            veeErrors.first("input-5")
          }}</b-form-invalid-feedback>
        </b-form-group>
      </b-form>
    </b-modal>

    <b-modal
      id="view-followers"
      ok-only
      ok-variant="secondary"
      ok-title="Dismiss"
			@ok="handleOkViewFollowers"
    >
      <b-overlay :show="userFollowLoading" opacity="0.95" rounded="sm">
				<b-tabs v-model="activeTab" class="following-tabs" content-class="mt-3" justified>
					<b-tab title="Following">
						<p v-if="user.following_count == 0">No users followed</p>
						<div v-for="(followRel, index) in followRels.following_rels" :key="index">
							<b-row>
								<user-card :user="followRel" :currentUser="currentUser" :index="index" :showFxns="true"/>
							</b-row>
						</div>
					</b-tab>
					<b-tab title="Followers">
						<p v-if="user.follower_count == 0">No followers</p>
						<div v-for="(followRel, index) in followRels.follower_rels" :key="index">
							<b-row>
								<user-card :user="followRel" :currentUser="currentUser" :index="index" :showFxns="false"/>
							</b-row>
						</div>
					</b-tab>
				</b-tabs>
      </b-overlay>
    </b-modal>

    <b-modal
      id="edit-spotify-account"
      title="Edit Spotify Account"
      ok-title="Save"
      @ok="handleOkSpotify"
    >
      <b-form @submit.stop.prevent="onSubmitSpotify" ref="form" v-if="show">
        <b-form-group
          id="input-group-1"
          label="Spotify Account"
          label-for="input-1"
        >
          <b-form-input
            id="input-1"
            name="input-1"
            v-model="form.spotify_account"
            type="text"
            placeholder="Enter spotify account"
            v-validate="{ required: true, min: 2 }"
            :state="validateState('input-1')"
            aria-describedby="input-1-live-feedback"
            data-vv-as="Spotify Account"
          ></b-form-input>
        </b-form-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import authHeader from "../../services/auth/auth-header";
import SongCard from "../../components/SongCard.vue";
import PostCard from "../../components/PostCard.vue";
import UserCard from "../../components/UserCard.vue";
export default {
  name: "Profile",
  components: {
    SongCard: SongCard,
    PostCard: PostCard,
		UserCard: UserCard
  },
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    },
    currentTheme() {
      return this.$store.state.theme;
    },
    appColor() {
      return this.$store.state.appColor;
    }
  },
  mounted() {
    if (!this.currentUser) {
      this.$router.push("/login");
    }
  },
  data() {
    return {
      selectedTheme: "",
      loading: true,
      message: "",
      successful: "",
      form: {
        firstname: "",
        lastname: "",
        email: "",
        username: "",
        spotify_account: "",
        bio: "",
      },
      user: {},
      show: true,
			userFollowLoading: false,
      songs: [],
      posts: [],
			followRels : {
				follower_rels: [],
				following_rels: []
			},
			activeTab: ''
    };
  },
  created() {
    this.getUserInfo();
    this.getUserPosts();
    this.getMusic();
    this.form.firstname = this.$store.state.auth.user.firstname;
    this.form.lastname = this.$store.state.auth.user.lastname;
    this.form.email = this.$store.state.auth.user.email;
    this.form.username = this.$store.state.auth.user.username;
    this.form.spotify_account = this.$store.state.auth.user.spotify_account;
    this.form.bio = this.$store.state.auth.user.bio;
  },
  watch: {
    appColor (newVal) {
      let avatarEl = document.getElementById('user-avatar');
			avatarEl.style = 'background-color:' + newVal;
    }
  },
  methods: {
    // TODO: Execute asynchronously in promise
    getUserInfo() {
      this.userProfileLoading = true;
      const path =
        "http://localhost/api/auth/get_user_info/" +
        this.$router.currentRoute.params.username;
      axios
        .get(path, {
          headers: authHeader(),
        })
        .then((res) => {
          this.user = res.data.userInfo;

					let appColor = this.user.appcolor ? this.user.appcolor : this.$store.state.defaultAppColor;
					let avatarEl = document.getElementById('user-avatar');
					avatarEl.style = 'background-color:' + appColor;
					avatarEl.classList.add('user-av');
          this.userProfileLoading = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUserPosts() {
      this.userPostsLoading = true;
      const path =
        "http://localhost/api/social/get_posts/" +
        this.$router.currentRoute.params.username;
      axios
        .get(path, {
          headers: authHeader(),
        })
        .then((res) => {
          this.posts = res.data;
          this.userPostsLoading = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getMusic() {
      const path =
        "http://localhost/api/music/get_music/" +
        this.$router.currentRoute.params.username;
      axios
        .get(path, {
          headers: authHeader(),
        })
        .then((res) => {
          this.songs = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    followUser() {
      const path = "http://localhost/api/social/follow_user";
      const data = {
        follower_username: this.currentUser.username,
        followed_username: this.user.username,
      };
      axios
        .post(path, data, {
          headers: authHeader(),
        })
        .then(() => {
          this.user.user_followed = true;
					this.getUserInfo();
        })
        .catch((error) => {
          console.error("Could not follow user", error);
        });
    },
    unfollowUser() {
      const path = "http://localhost/api/social/unfollow_user";
      const data = {
        follower_username: this.currentUser.username,
        followed_username: this.user.username,
      };
      axios
        .post(path, data, {
          headers: authHeader(),
        })
        .then(() => {
          this.user.user_followed = false;
					this.getUserInfo();
        })
        .catch((error) => {
          console.error("Could not unfollow user", error);
        });
    },
    getFollowRels(activateTab) {
			this.activeTab = activateTab;
      this.userFollowLoading = true;
      const path =
        "http://localhost/api/social/relationship/" +
        this.$router.currentRoute.params.username;
      axios
        .get(path, {
          headers: authHeader(),
        })
        .then((res) => {
          this.followRels = res.data;
          this.userFollowLoading = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    editProfile() {
      this.$router.push("/editProfile");
    },
    onSubmit() {
      this.loading = true;
      this.$validator.validateAll().then((isValid) => {
        if (!isValid) {
          this.loading = false;
          return;
        }

        if (this.form.email && this.form.username) {
          this.$store.dispatch("auth/updateProfile", this.form).then(
            () => {
              // Hide the modal manually
              this.$nextTick(() => {
                this.$bvModal.hide("edit-profile");
              });
            },
            (error) => {
              this.loading = false;
              this.successful = false;
              this.message =
                (error.response && error.response.data) ||
                error.message ||
                error.toString();
            }
          );
        }
      });
    },
    onSubmitSpotify() {
      this.loading = false;
      if (this.form.spotify_account) {
        this.$store.dispatch("auth/updateSpotifyAccount", this.form).then(
          () => {
            // Hide the modal manually
            this.$nextTick(() => {
              this.$bvModal.hide("edit-spotify-account");
            });
          },
          (error) => {
            this.loading = false;
            this.successful = false;
            this.message =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
        );
      }
    },
    validateState(ref) {
      if (
        this.veeFields[ref] &&
        (this.veeFields[ref].dirty || this.veeFields[ref].validated)
      ) {
        return !this.veeErrors.has(ref);
      }
      return null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.onSubmit();
    },
    handleOkSpotify(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.onSubmitSpotify();
    },
		handleOkViewFollowers(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.getUserInfo();
			// Hide the modal manually
			this.$nextTick(() => {
				this.$bvModal.hide("view-followers");
			});
    },
    getAvatarText() {
      try {
        let firstInitial = this.user.firstname.charAt(0);
        let lastInitial = this.user.lastname.charAt(0);
        return firstInitial.toUpperCase() + lastInitial.toUpperCase();
      } catch (err) {
        return "";
      }
    },
  },
};
</script>

<style scoped>
.edit-profile {
  text-align: right;
}

.avatar-row {
  align-items: center;
}

.display-name {
  padding-top: 10px;
}

.display-name > span {
  font-size: 2rem;
}

.display-name > div {
  padding-left: 0;
}

.bio {
  padding-top: 5px;
}

.following-tabs {
	overflow-x: hidden !important;
}

.user-av {
	width: 6rem;
	height: 6rem;
}
</style>