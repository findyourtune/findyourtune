<template>
  <b-container class="suggested-people-card">
    <b-card>
      <b-row>
        <b-col>
          <div>{{person.user_firstname}}</div>
        </b-col>
      </b-row>
    </b-card>
  </b-container>
</template>

<script>
export default {
  name: "SuggestedPeople",
  props: {
    person: {
      type: Object,
    },
  },
};
</script>

<style scoped>
.suggested-people-card {
  padding-bottom: 10px;
}
</style>