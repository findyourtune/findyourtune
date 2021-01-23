<template>
    <div class="container">
        <h1>Test API</h1>
        <hr>
        <button type="button" class="btn btn-success btn-sm">Add Course</button>
        <table class="table table-hover">
            <tr>
                <th scope="col">Title</th>
                <th scope="col">Author</th>
                <th scope="col">Paperback</th>
            </tr>
            <tbody>
            <tr v-for="(course, index) in courses" :key="index">
                <td>{{ course.title }}</td>
                <td>{{ course.author }}</td>
                <td>
                <span v-if="course.paperback">Yes</span>
                <span v-else>No</span>
                </td>
                <td>
                <button type="button" class="btn btn-info btn-sm">Update</button>
                <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </td>
            </tr>
            </tbody>
        </table>
      <div class="columns">
        <div class="column">
          <theme-picker class="column"/>
        </div>
        <div class="column is-three-quarters">
          <themed-title>Examples of Themed Components</themed-title>
          <themed-btn>Themed Button</themed-btn>
          <themed-btn>Another Themed Button</themed-btn>
        </div>
      </div>
    </div>
</template>

<script>
 import axios from 'axios';
 import authHeader from '../services/auth/auth-header';
 import ThemePicker from '@/components/ThemePicker';
 
 export default {
  name: 'Courses',
  components: {
       'ThemePicker': ThemePicker
   },
  data() {
    return {
      courses: [],
    };
  },
  computed: { // Returns stored user info and assigns to currentUser object
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    getCourses() {
      const path = 'http://localhost/api/testapi';
      axios.get(path, { headers: authHeader() })
        .then((res) => {
          this.courses = res.data.courses;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getCourses();
  },
  mounted() { // If user isn't logged in, send them to /login
    if (!this.currentUser) {
      this.$router.push('/login');
    }
  },
 };
 </script>