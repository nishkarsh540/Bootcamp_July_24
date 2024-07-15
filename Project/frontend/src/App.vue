<template>
  <div id="app">
      <template v-if="isAuthenticated">
        <template v-if="userRole === 'admin'">
          <router-link to="/admin-dashboard"> Admin Dashboard</router-link>
        </template>
        <template v-if="userRole === 'user'">
          <router-link to="/user-dashboard"> User Dashboard</router-link>
        </template>
        <button @click="logout">Logout</button>
      </template>
      <template v-if ='!isAuthenticated'>
        <router-link to="/login">Login</router-link>
        <router-link to="/signup">Singup</router-link>
      </template>
      <router-view/>
  </div>
  
</template>

<script>
import {mapGetters,mapActions} from 'vuex';

export default{
  name:'App',
  computed:{
    ...mapGetters(['isAuthenticated','userRole'])
  },
  methods:{
    ...mapActions(['logout'])
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
