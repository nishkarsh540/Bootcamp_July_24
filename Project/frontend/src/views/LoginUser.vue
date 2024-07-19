<template>
  <div class="login-container">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <div v-if="errorMessage">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          username: this.username,
          password: this.password
        });
        const { access_token, user } = response.data;

        // Update Vuex store instead of directly updating localStorage
        this.$store.dispatch('login', { token: access_token, user });

        // Navigate based on user role
        if (user.role === 'admin') {
          this.$router.push('/admin-dashboard');
        } else if (user.role === 'store_manager') {
          this.$router.push('/store-dashboard');
        } else {
          this.$router.push('/user-dashboard');
        }
      } catch (error) {
        this.errorMessage = error.response ? error.response.data.message:'Invalid Username or Password';
      }
    }
  }
};
</script>
