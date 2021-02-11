import Vue from 'vue';

// Themed Button
import ThemedButton from './ThemedButton';

export const themedButton = Vue.component('themed-btn', {
    components: { ThemedButton },
    template: `<ThemedButton :color="$store.getters['appColor']" class="button"><slot></slot></ThemedButton>`,
});

// Themed Title
import ThemedTitle from './ThemedTitle';

export const themedTitle = Vue.component('themed-title', {
    components: { ThemedTitle },
    template: `<ThemedTitle :color="$store.getters['appColor']"><slot></slot></ThemedTitle>`,
});

// Themed Divider
import ThemedDivider from './ThemedDivider';

export const themedDivider = Vue.component('themed-divider', {
    components: { ThemedDivider },
    template: `<ThemedDivider :color="$store.getters['appColor']"><slot></slot></ThemedDivider>`,
});
