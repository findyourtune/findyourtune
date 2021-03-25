<template>
  <div id="header">
    <div id="headerContent">
      <b-row class="header-row">
        <b-col cols="2">
          Logo Here
        </b-col>

        <b-col cols="8"></b-col>

        <b-col cols="2">
          <b-dropdown size="lg" right variant="link" toggle-class="text-decoration-none" no-caret>
            <template #button-content>
              <b-icon class="settings-gear" icon="display" aria-hidden="true"></b-icon>
            </template>
            <b-dropdown-text>
              <b-row class="background-area">
                <b-col cols="7">
                  Background:
                </b-col>
                <b-col cols="5">
                  <label class="switch">
                    <input id="themeToggle" type="checkbox" @click="toggleTheme()">
                    <span class="slider round"></span>
                  </label>
                </b-col>
              </b-row>
              <b-dropdown-divider class="dropdown-divider" v-if="currentUser"></b-dropdown-divider>
              <b-row class="appcolor-area" v-if="currentUser">
                <b-col cols="7">
                  Color:
                </b-col>
                <b-col cols="5">
                  <app-color-picker/>
                </b-col>
              </b-row>
            </b-dropdown-text>
          </b-dropdown>

          <a v-if="currentUser" class="logout" @click="logout()">Logout</a>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import { mapMutations } from 'vuex';
import AppColorPicker from '@/components/AppColorPicker';
export default {
    name: 'Header',
    components: {
       'AppColorPicker': AppColorPicker
   },
    data() {
      return {
        checked: null
      };
    },
    computed: {
      currentUser() {
        return this.$store.state.auth.user;
      },
      currentTheme() {
        return this.$store.state.theme;
      }
    },
    methods: {
      ...mapMutations([
      'toggleTheme',
      'setDefaultAppColor'
      ]),
      logout() {
        this.$store.dispatch('auth/logout');
        this.setDefaultAppColor();
        this.$router.push('/login');
      },
    },
    mounted() {
      if (this.currentTheme == 'light'){
        this.checked = false;
      } else {
        this.checked = true;
      }

      if (this.currentTheme == 'light') {
          document.getElementById("themeToggle").checked = false;
      } else {
          document.getElementById("themeToggle").checked = true;
      }
    },  
}
</script>

<style scoped>
#header {
  height: 60px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--app-color);
}

#headerContent {
  margin-left: 10px;
  width: 100%;
}

.background-area {
  padding-top: 10px;
}

.appcolor-area {
  align-items: center;
  padding-top: 5px;
}

.header-row > div {
  display: flex;
  align-items: center;
}
</style>