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
    mounted() {
      // Check local storage for login status on component mount
      const storedLoginStatus = localStorage.getItem('isLoggedIn');
      if (storedLoginStatus) {
        this.isLoggedIn = JSON.parse(storedLoginStatus);
      }
    },

    methods: {
        updateLoginStatus(status) {
          this.isLoggedIn = status;
          // Update local storage with the new login status
          localStorage.setItem('isLoggedIn', JSON.stringify(status));
        },

        handleLogout() {
          this.isLoggedIn = false;
          // Clear the login status from local storage on logout
          localStorage.removeItem('isLoggedIn');
        },
    },

  }
</script>

<style>
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
