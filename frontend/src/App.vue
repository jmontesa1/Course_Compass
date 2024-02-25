<template>
  <!-- Display the navbar and the router view on every page -->
  <NavBar :isLoggedIn="isLoggedIn" @logout="handleLogout"/>
  <router-view @login-status-changed="updateLoginStatus" @show-toast="showToastMessage" :user="user" />
  <Footer></Footer>
  <Toast :showToast="showToast" :toastMessage="toastMessage" />


</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import Footer from '@/components/Footer.vue'
  import Toast from '@/components/Toast.vue'

  export default{
    name: 'App',
    components: {
      NavBar,
      Footer,
      Toast,
    },

    data() {
        return {
            isLoggedIn: false,
            showToast: false,
            toastMessage: "",
            user: {},
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

        showToastMessage(message){
                this.toastMessage = message;
                this.showToast = true;
                setTimeout(() => {
                    this.showToast = false;
                },5000);
            }
    },

  }
</script>

<style>
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
