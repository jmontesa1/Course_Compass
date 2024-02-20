<template>
  <!-- Display the navbar and the router view on every page -->
  <NavBar :isLoggedIn="isLoggedIn" @logout="handleLogout"/>
  <router-view @login-status-changed="updateLoginStatus" />
  <Footer></Footer>
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import Footer from '@/components/Footer.vue'

  export default{
    name: 'App',
    components: {
      NavBar,
      Footer,
    },

    data() {
        return {
            isLoggedIn: false,
        };
    },
    methods: {
        updateLoginStatus(status) {
            this.isLoggedIn = status;
        },
        
        handleLogout() {
          this.isLoggedIn = false;
        },
    },

  }
</script>

<style>
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
