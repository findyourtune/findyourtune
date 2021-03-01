<template>
  <b-container class="post-card">
      <b-card>
        <b-row>
            {{post.text}}
        </b-row>
        <b-row>
            {{post.name}}
        </b-row>
      </b-card>
  </b-container>
</template>

<script>
export default {
    name: 'PostCard',
    props: {
        post: {
            type: Object
        }  
    },
};
</script>

<style>
.post-card {
    padding-top: 10px;
}
</style>