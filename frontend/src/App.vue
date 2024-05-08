<!--Creates the base of the softwares frontend-->
<template>
  <!-- Display the navbar and the router view on every page -->
  <NavBar :userType="userType" :isLoggedIn="isLoggedIn" @logout="handleLogout" />
  <!-- Everypage draws specific variables that can be used, emits certain events to determine login status or toasts -->
  <router-view :userType="userType" @login-status-changed="updateLoginStatus" @show-toast="showToastMessage" @update-user-type="updateUserType" />
  <Footer></Footer> <!-- Footer displayed -->
  <Toast :showToast="showToast" :toastMessage="toastMessage" :toastColor="toastColor" /> <!-- Every page can utilize toasts -->
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
            userType: '',
            showToast: false,
            toastMessage: "",
            toastColor: '#da4d4d',
        };
    },

    mounted() {
      // Check local storage for login status on component mount
      const storedLoginStatus = localStorage.getItem('isLoggedIn');
      if (storedLoginStatus) {
        this.isLoggedIn = JSON.parse(storedLoginStatus);
      }
      
      // Check local storage for user type on component mount
      const storedUserType = localStorage.getItem('userType');
      if (storedUserType) {
        this.userType = storedUserType;
        this.$emit('update-user-type', storedUserType);
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
          this.userType = '';
          // Clear the login status from local storage on logout
          localStorage.removeItem('isLoggedIn');
          localStorage.removeItem('userType');
        },

        //Shows toasts and message/color depending on event emitted in component
        showToastMessage(payload){
                this.toastMessage = payload.message;
                this.toastColor = payload.color;
                this.showToast = true;
                setTimeout(() => {
                    this.showToast = false;
                },5000);
            },
        
        updateUserType(userType) {
          this.userType = userType;
          // Update local storage with the user type
          localStorage.setItem('userType', userType);
          this.$emit('update-user-type', userType); 
        },
    },

  }
</script>

<style>
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>