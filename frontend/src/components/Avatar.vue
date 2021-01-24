<template>
  <b-avatar variant="info" :text="getAvatarText()" size="6rem"></b-avatar>
</template>

<script>
export default {
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    getAvatarText() {
        let firstInitial = this.currentUser.firstname.charAt(0);
        let lastInitial = this.currentUser.lastname.charAt(0);
        return firstInitial.toUpperCase() + lastInitial.toUpperCase();
    }
  },
};
</script>

<style>
</style>