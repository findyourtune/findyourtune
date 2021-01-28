<template>
  <v-swatches
    :value="appColor"
    :swatches="swatches"
    row-length="4"
    popover-x="right"
    @input="setAppColor($event)"
    :background-color="themeColor"
  ></v-swatches>
</template>

<script>
import VSwatches from 'vue-swatches'
import 'vue-swatches/dist/vue-swatches.css'
import { mapGetters, mapMutations } from 'vuex';
export default {
  components: { VSwatches },
  data() {
    return {
      color: '#1CA085',
      // Pastel
      swatches: [
        ['#ffadad', '#ffd6a5', '#fdffb6', '#caffbf'],
        ['#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff']
      ]
      // Rainbow
      // swatches: [
      //   ['#e6261f', '#eb7532', '#f7d038', '#a3e048'],
      //   ['#49da9a', '#34bbe6', '#4355db', '#bf53ce']
      // ]
    }
  },
  computed: {
    ...mapGetters([
      'appColor',
      'themeColor'
    ])
  },
  methods: {
    ...mapMutations([
      'setAppColor'
    ]),
  },
  watch: {
    themeColor() {}
  }
};
</script>

<style>
</style>