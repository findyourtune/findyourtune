import Vue from 'vue';

import ThemedButton from './ThemedButton';

export const themedButton = Vue.component('themed-btn', {
    components: { ThemedButton },
    template: `<ThemedButton :color="$store.getters['themeColor']" class="button"><slot></slot></ThemedButton>`,
});

import ThemedTitle from './ThemedTitle';

export const themedTitle = Vue.component('themed-title', {
    components: { ThemedTitle },
    template: `<ThemedTitle :color="$store.getters['themeColor']"><slot></slot></ThemedTitle>`,
});