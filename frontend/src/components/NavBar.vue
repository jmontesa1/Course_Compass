<!-- Created by: John Montesa -->
<!-- This component creates the navigation bar that the user will interact with -->
<!-- There are 5 buttons, and one is a drop down menu that directs the user to log in, sign up, or check their profile settings-->

<template>
    <v-banner v-if="isBannerVisible" color="grey-darken-1" icon="mdi-account-box" lines="two">
        <template v-slot:prepend>
            <span class="material-icons" style="color:white">notifications</span>
        </template>

        <v-banner-text class="notification-text">
            <b> {{ upcomingNotification.date }} </b> {{ upcomingNotification.source }} - {{ upcomingNotification.message }}
        </v-banner-text>

        <v-banner-actions class="notification-actions">
            <v-btn class ="notification-button" @click="dismissBanner">
                <span class="material-icons" style="color:white">close</span>
            </v-btn>
        </v-banner-actions>
    </v-banner>


    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
                <router-link to="/" class="navbar-brand">
                    <img src="../assets/course compass logo.png" alt="Course Compass Logo">
                </router-link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <!-- right-aligned menu items -->
                    <li class="nav-item">
                        <router-link to="/courses" class = "nav-link">Courses</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/schedule" class = "nav-link">Schedule</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/progress" class = "nav-link">Progress</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/about" class = "nav-link">About</router-link>
                    </li>
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            Account
                        </a>
                        <ul class="dropdown-menu">
                            <li><router-link to="/login" class = "dropdown-item">Log in</router-link></li>
                            <li><router-link to="/signup" class = "dropdown-item">Sign Up</router-link></li>
                            <li><router-link to="/myaccount" class = "dropdown-item">My Account</router-link></li>
                            <li><a href="#" class="dropdown-item" @click.prevent="handleLogout">Log Out</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
    import axios from 'axios';

    export default{
        data(){
            return{
                isBannerVisible: true,
                notifications: [
                    {date: '5/15/2024', source: 'UNR', message: 'Instruction Ends'},
                    {date: '3/1/2024', source: 'UNR', message: 'Deadline to apply for May graduation'},
                ],
                currentDate : null,
            };
        },

        computed:{
            upcomingNotification(){
                //this.currentDate = new Date('2024-03-03'); //USE THIS AS A TEST CASE TO CHECK DIFFERENT DAYS, THIS SHOWS IT WORKS WHEN A DAY PASSES FOR A NOTIF
                //this.currentDate = new Date(); //get current day
                const upcomingNotifications = this.notifications.filter(notification => new Date(notification.date) > this.currentDate).sort((a, b) => new Date(a.date) - new Date(b.date));

                return upcomingNotifications.length > 0 ? upcomingNotifications[0] : null;
            },
        },

        methods:{
            dismissBanner(){
                this.isBannerVisible = false;
            },
            
            handleLogout() {
                axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true })
                    .then(response => {
                        console.log(response.data.message);
                        if (response.status === 200) {
                        setTimeout(() => {
                            this.$router.push('/');
                        }, 2500);
                        } else {
                            console.error("Unexpected response during logout: ", response);
                        }
                    })
                    .catch(error => {
                        console.error("Logout error: ", error);
                    });
            },
        },
    };
</script>

<style scoped>
    .navbar {
        background-color: #ffffff; 
        border-bottom: 1px solid #000000;
    }

    .navbar-brand img {
        max-width: 85px;
        height: auto;
        margin: -8px auto;
    }

    .nav-link {
        font-family: 'coolvetica';            
        font-size: 25px;
        color: #160e0e;
        margin-right: 10px;
    }

    .nav-link:hover {
        color: #ffffff;
        background-color: #000000;
        margin-top: -5px;
        margin-bottom: -5px;
    }

    .dropdown-menu {
        font-family: 'coolvetica';
        background-color: #ffffff00;
        border: 1px solid transparent;
        text-align: center;
        font-size: 15px;
        min-width: 130px;
    }

    .dropdown-item {
        color: #000000;
        border: 1px solid #000000;
        text-align: center;
        background-color: #ffffff;
    }

    .dropdown-item:hover {
        color: #ffffff;
        background-color: #000000;
    }

    .v-banner{
        margin-top: -5px; /* Adjust the maximum width as needed */
        margin-bottom: -20px;
        background-color: rgb(53, 53, 53);
    }

    .notification-actions{
        margin-left: auto;
    }

    .notification-button:hover{
        background-color:rgb(157, 157, 157);
    }

    .notification-text{
        font-family: Poppins;
        color: rgb(185, 185, 185);
    }

    .notification-button{
        transform: translate(-15px, -22px);
    }

</style>
