<template>
  <!-- Display the navbar and the router view on every page -->
  <NavBar></NavBar>
  <router-view/>
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
    }
  }
</script>

<style>
  nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
